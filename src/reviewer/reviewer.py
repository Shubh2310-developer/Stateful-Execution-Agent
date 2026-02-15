from typing import Any, Dict, List, Optional
from src.core.types import TaskState, Step
from src.reviewer.quality_checker import QualityChecker
from src.reviewer.success_validator import SuccessValidator
from src.executor.artifact_manager import ArtifactManager
from src.executor.step_runner import StepRunner
from src.trace.trace_logger import trace_logger
from src.trace.decision_recorder import decision_recorder
from src.memory.learning.feedback_processor import FeedbackProcessor
from src.utils.logger import logger
from src.llm.prompt_builder import prompt_builder
from src.llm.groq_client import groq_client
from src.llm.response_parser import ResponseParser


class Reviewer:
    """
    Orchestrates the review and validation of task execution with self-correction loop.

    This reviewer acts as a critical editor that:
    1. Evaluates task completion against original goal and success criteria
    2. Runs hybrid quality checks (static + LLM)
    3. Determines if work passes or needs revision
    4. Sends tasks back to Executor with specific revision instructions (up to max_iterations)
    """

    # Default iteration limit to prevent infinite loops
    DEFAULT_MAX_ITERATIONS = 2

    # Quality threshold for automatic pass
    QUALITY_PASS_THRESHOLD = 70.0

    def __init__(self, max_iterations: int = DEFAULT_MAX_ITERATIONS):
        """
        Initialize the Reviewer.

        Args:
            max_iterations: Maximum number of revision iterations (default: 2)
        """
        self.quality_checker = QualityChecker()
        self.success_validator = SuccessValidator()
        self.artifact_manager = ArtifactManager()
        self.step_runner = StepRunner(self.artifact_manager)
        self.max_iterations = max_iterations

    async def review_task(
        self,
        state: TaskState,
        iteration_count: int = 0,
        previous_feedback: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Performs a comprehensive review of task execution.

        This is the primary entry point for task evaluation. It runs end-to-end
        semantic analysis, artifact-specific quality checks, and success criteria
        validation to determine if the task requires revision.

        Args:
            state (TaskState): The current state of the task, including produced artifacts.
            iteration_count (int, optional): The current revision iteration (0 for initial review).
                Defaults to 0.
            previous_feedback (str, optional): Feedback from a previous review pass to guide
                evaluation of improvements. Defaults to None.

        Returns:
            Dict[str, Any]: A detailed review report containing success status, quality scores,
                revision instructions, and qualitative assessment.
        """
        logger.info(
            f"Starting review for task {state.task_id} (iteration {iteration_count}/{self.max_iterations})"
        )
        
        await trace_logger.log_event(
            event_type="review_start",
            context={"iteration": iteration_count, "max_iterations": self.max_iterations},
            task_id=state.task_id
        )

        try:
            # 1. Collect and prepare artifacts
            artifact_list = await self._prepare_artifacts(state)

            # 2. Run end-to-end LLM review
            review_result = await self._run_llm_review(
                state,
                artifact_list,
                iteration_count,
                previous_feedback
            )

            # 2.5 Run semantic success validation
            success_report = await self.success_validator.validate_achievement_llm(state)

            # 3. Run detailed quality checks on each artifact
            quality_reports = await self._run_quality_checks(state)

            # 4. Calculate overall quality score
            overall_quality_score = self._calculate_overall_quality_score(
                review_result,
                quality_reports
            )

            # 5. Determine if revision is needed
            # Use both LLM review and semantic success check to decide
            needs_revision = self._should_revise(
                review_result,
                overall_quality_score,
                iteration_count
            ) or not success_report.get("achieved", True)

            # 6. Build comprehensive result
            result = {
                "task_id": state.task_id,
                "overall_success": success_report.get("achieved", review_result.get("overall_success", False)),
                "needs_revision": needs_revision,
                "quality_score": overall_quality_score,
                "completion_report": success_report,
                "quality_breakdown": {
                    "llm_review_score": review_result.get("quality_score", 0),
                    "artifact_quality_scores": {
                        aid: qr.get("quality_score", 0)
                        for aid, qr in quality_reports.items()
                    },
                    "static_checks": self._extract_static_checks(quality_reports),
                    "llm_checks": self._extract_llm_checks(quality_reports)
                },
                "requirement_coverage": review_result.get("requirement_coverage", {}),
                "success_criteria_status": review_result.get("success_criteria_status", []),
                "artifact_assessment": review_result.get("artifact_assessment", []),
                "strengths": review_result.get("strengths", []),
                "weaknesses": review_result.get("weaknesses", []),
                "revision_instructions": review_result.get("revision_instructions", []),
                "feedback": review_result.get("feedback", ""),
                "recommendations": review_result.get("recommendations", []),
                "iteration_count": iteration_count,
                "artifact_quality": quality_reports,
                "reasoning": review_result.get("reasoning", "No reasoning provided")
            }

            # Log iteration summary
            self._log_iteration_summary(result)
            
            # Record review decision with trace
            await decision_recorder.record_decision(
                decision_point="review_completion",
                rationale=result.get("reasoning", "Review completed"),
                final_choice="pass" if result["overall_success"] and not result["needs_revision"] else "needs_revision",
                task_id=state.task_id,
                confidence_score=result["quality_score"] / 100.0,
                metadata={
                    "iteration": iteration_count,
                    "quality_score": result["quality_score"],
                    "needs_revision": result["needs_revision"]
                }
            )
            
            await trace_logger.log_event(
                event_type="review_complete",
                context={"success": result["overall_success"], "quality_score": result["quality_score"]},
                task_id=state.task_id,
                outcome={"needs_revision": result["needs_revision"]}
            )

            return result

        except Exception as e:
            logger.error(f"Review failed for task {state.task_id}: {str(e)}")
            
            await trace_logger.log_event(
                event_type="review_error",
                context={"error": str(e)},
                task_id=state.task_id
            )
            
            return {
                "task_id": state.task_id,
                "overall_success": False,
                "needs_revision": False,  # Don't retry on error
                "quality_score": 0.0,
                "error": str(e),
                "iteration_count": iteration_count
            }

    async def review_with_correction_loop(
        self,
        state: TaskState,
        user_memory: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Orchestrates the complete review-revision cycle automatically.

        This method performs a review, and if improvements are needed and iterations
        are available, it instructs the Executor to re-run specific steps with
        corrective guidance, recursively repeating the process until completion or
        limit reached.

        Args:
            state (TaskState): The current task state to be reviewed and potentially revised.
            user_memory (Any, optional): Context from user history for the executor.
                Defaults to None.

        Returns:
            Dict[str, Any]: The final review results after all iteration cycles are complete.
        """
        iteration = 0
        previous_feedback = None

        while iteration <= self.max_iterations:
            # Run review
            review_result = await self.review_task(
                state,
                iteration_count=iteration,
                previous_feedback=previous_feedback
            )

            # Check if we're done (passed or max iterations reached)
            if not review_result.get("needs_revision", False):
                logger.info(
                    f"Task {state.task_id} review complete: "
                    f"Success={review_result['overall_success']}, "
                    f"Score={review_result['quality_score']:.1f}"
                )
                return review_result

            if iteration >= self.max_iterations:
                logger.warning(
                    f"Task {state.task_id} reached max iterations ({self.max_iterations}). "
                    f"Final score: {review_result['quality_score']:.1f}"
                )
                # Mark as no longer needing revision (we're out of attempts)
                review_result["needs_revision"] = False
                review_result["feedback"] += f"\n\nWARNING: Max iterations ({self.max_iterations}) reached. No further revisions attempted."
                return review_result

            # Revision needed and we have iterations left
            logger.info(
                f"Task {state.task_id} needs revision. "
                f"Iteration {iteration + 1}/{self.max_iterations}"
            )

            # Execute revision with Executor
            revision_success = await self._execute_revision(
                state,
                review_result,
                user_memory
            )

            if not revision_success:
                logger.error(f"Revision execution failed for task {state.task_id}")
                review_result["needs_revision"] = False
                review_result["error"] = "Revision execution failed"
                return review_result

            # Prepare for next iteration
            iteration += 1
            previous_feedback = review_result.get("feedback", "")

        # Should not reach here, but safety return
        return review_result

    async def _prepare_artifacts(self, state: TaskState) -> List[Dict[str, Any]]:
        """
        Prepares and summarizes artifact data for efficient LLM processing.

        Args:
            state (TaskState): Current state.

        Returns:
            List[Dict[str, Any]]: List of artifact metadata and content previews.
        """
        artifact_list = []

        for artifact in state.artifacts:
            art_data = artifact.dict()

            # Include content preview for reviewable types
            if artifact.type in ["document", "data", "code"]:
                try:
                    content = self.artifact_manager.get_artifact_content(artifact)
                    content_str = str(content)
                    # Truncate long content
                    max_preview = 2000
                    if len(content_str) > max_preview:
                        art_data["content_preview"] = content_str[:max_preview] + "\n...[truncated]"
                    else:
                        art_data["content_preview"] = content_str
                except Exception as e:
                    logger.warning(f"Could not load content for artifact {artifact.id}: {e}")
                    art_data["content_preview"] = f"[Error loading content: {str(e)}]"

            artifact_list.append(art_data)

        return artifact_list

    async def _run_llm_review(
        self,
        state: TaskState,
        artifact_list: List[Dict[str, Any]],
        iteration_count: int,
        previous_feedback: Optional[str]
    ) -> Dict[str, Any]:
        """
        Executes the main semantic review using an LLM.

        Args:
            state (TaskState): Task state.
            artifact_list (List[Dict[str, Any]]): Prepared artifact summaries.
            iteration_count (int): Current revision cycle.
            previous_feedback (str, optional): Previous reviewer notes.

        Returns:
            Dict[str, Any]: Raw JSON response from the LLM reviewer.
        """
        # Build review prompt
        messages = prompt_builder.build_reviewer_prompt(
            goal=state.goal.dict(),
            plan_steps=[s.dict() for s in state.plan.steps] if state.plan else [],
            artifacts=artifact_list,
            iteration_count=iteration_count,
            previous_feedback=previous_feedback
        )

        try:
            response_text = await groq_client.generate_response(messages)
            review_result = ResponseParser.parse_json_response(response_text)

            # Log the reasoning
            reasoning = review_result.get("reasoning", "No reasoning provided")
            logger.info(f"Reviewer Reasoning:\n{reasoning[:500]}...")

            return review_result

        except Exception as e:
            logger.error(f"LLM review failed: {str(e)}")
            # Return minimal failure result
            return {
                "overall_success": False,
                "quality_score": 0,
                "needs_revision": True,
                "feedback": f"Review failed: {str(e)}",
                "revision_instructions": ["Manual review required - automated review failed"],
                "error": str(e)
            }

    async def _run_quality_checks(self, state: TaskState) -> Dict[str, Dict[str, Any]]:
        """
        Orchestrates artifact-level quality checks using the QualityChecker.

        Args:
            state (TaskState): Task state.

        Returns:
            Dict[str, Dict[str, Any]]: Mapping of artifact IDs to their quality reports.
        """
        quality_reports = {}

        for artifact in state.artifacts:
            if artifact.type in ["document", "data", "code"]:
                try:
                    content = self.artifact_manager.get_artifact_content(artifact)

                    # Extract success criteria for this artifact's step
                    success_criteria = self._get_step_success_criteria(state, artifact.step_id)

                    report = await self.quality_checker.check_quality(
                        artifact,
                        content,
                        success_criteria
                    )
                    quality_reports[artifact.id] = report

                except Exception as e:
                    logger.error(f"Quality check failed for artifact {artifact.id}: {e}")
                    quality_reports[artifact.id] = {
                        "quality_score": 0.0,
                        "error": str(e)
                    }

        return quality_reports

    def _get_step_success_criteria(
        self,
        state: TaskState,
        step_id: Optional[str]
    ) -> Optional[List[str]]:
        """
        Extracts the success criteria associated with a specific step ID.

        Args:
            state (TaskState): Current state.
            step_id (str, optional): The ID of the step.

        Returns:
            List[str], optional: Success criteria if found, else None.
        """
        if not state.plan or not step_id:
            return None

        for step in state.plan.steps:
            if getattr(step, 'id', getattr(step, 'step_id', None)) == step_id:
                criteria = getattr(step, 'success_criteria', None)
                if criteria:
                    return [criteria] if isinstance(criteria, str) else criteria

        return None

    def _calculate_overall_quality_score(
        self,
        review_result: Dict[str, Any],
        quality_reports: Dict[str, Dict[str, Any]]
    ) -> float:
        """
        Calculates a final weighted quality score for the entire task.

        Combines the end-to-end LLM review score (60%) with the average of
        individual artifact quality checks (40%).

        Args:
            review_result (Dict[str, Any]): Result from the LLM review pass.
            quality_reports (Dict[str, Dict[str, Any]]): Artifact quality checks.

        Returns:
            float: A weighted score between 0 and 100.
        """
        llm_score = review_result.get("quality_score", 0)

        # Calculate average artifact quality
        artifact_scores = [
            qr.get("quality_score", 0)
            for qr in quality_reports.values()
            if "quality_score" in qr
        ]
        avg_artifact_score = sum(artifact_scores) / len(artifact_scores) if artifact_scores else 0

        # Weighted combination
        overall_score = (llm_score * 0.6) + (avg_artifact_score * 0.4)

        return round(overall_score, 2)

    def _should_revise(
        self,
        review_result: Dict[str, Any],
        overall_quality_score: float,
        iteration_count: int
    ) -> bool:
        """
        Determines if a task requires a revision pass.

        Logic:
        1. If iterations are exhausted, return False.
        2. If LLM review explicitly requests revision, return True.
        3. If quality score is below 70.0, return True.
        4. If overall success flag is false, return True.

        Args:
            review_result (Dict[str, Any]): semantic review pass result.
            overall_quality_score (float): Calculated task quality.
            iteration_count (int): Current iteration.

        Returns:
            bool: True if revision is necessary and possible.
        """
        if iteration_count >= self.max_iterations:
            return False

        # Check explicit needs_revision flag
        explicit_revision = review_result.get("needs_revision", False)

        # Check quality threshold
        below_threshold = overall_quality_score < self.QUALITY_PASS_THRESHOLD

        # Check success flag
        not_successful = not review_result.get("overall_success", False)

        return explicit_revision or below_threshold or not_successful

    async def _execute_revision(
        self,
        state: TaskState,
        review_result: Dict[str, Any],
        user_memory: Optional[Any]
    ) -> bool:
        """
        Coordinates the Executor to re-run steps with reviewer guidance.

        Args:
            state (TaskState): Current state.
            review_result (Dict[str, Any]): Result from the review pass containing instructions.
            user_memory (Any, optional): Context for the executor.

        Returns:
            bool: True if revision was executed successfully.
        """
        try:
            # Identify which steps need revision
            steps_to_revise = self._identify_steps_to_revise(state, review_result)

            if not steps_to_revise:
                logger.warning("No steps identified for revision")
                return False

            logger.info(f"Re-executing {len(steps_to_revise)} steps for revision")

            # For each step, call step_runner with revision context
            for step in steps_to_revise:
                step_id = getattr(step, 'id', getattr(step, 'step_id', None))

                # Get step artifacts for context
                step_artifacts = [
                    art for art in state.artifacts
                    if art.step_id == step_id
                ]

                # Prepare artifact data for revision prompt
                artifact_preview = {}
                for art in state.artifacts:
                    try:
                        content = self.artifact_manager.get_artifact_content(art)
                        artifact_preview[art.id] = str(content)[:1000]
                    except:
                        pass

                # Build revision prompt using the dedicated prompt builder method
                messages = prompt_builder.build_revision_prompt(
                    step=step,
                    artifacts=[art.dict() for art in step_artifacts],
                    revision_instructions=review_result.get("revision_instructions", []),
                    weaknesses=review_result.get("weaknesses", []),
                    quality_score=review_result.get("quality_score", 0),
                    needs_revision=True,
                    requirement_coverage=review_result.get("requirement_coverage"),
                    available_artifacts=artifact_preview,
                    tool_list=self.step_runner.tool_orchestrator.tool_selector.get_available_tool_names(),
                    user_preferences=getattr(user_memory, 'preferences', None) if user_memory else None
                )

                # Re-run the step logic with the revision messages
                response_text = await groq_client.generate_response(messages)
                execution_decision = ResponseParser.parse_json_response(response_text)

                action, params = ResponseParser.extract_action_and_params(execution_decision)

                # Execute the tool
                tool_output = await self.step_runner.tool_orchestrator.invoke_tool(
                    action,
                    params,
                    available_artifacts=state.artifacts,
                    user_memory=user_memory
                )

                # Create a new artifact for the revision
                new_artifact = await self.artifact_manager.create_artifact(
                    task_id=state.task_id,
                    step_id=step_id,
                    artifact_type="data",
                    content=tool_output,
                    format="json",
                    metadata={
                        "is_revision": True,
                        "iteration": review_result.get("iteration_count", 0) + 1,
                        "reviewer_feedback": review_result.get("feedback")
                    }
                )

                # Update state with new artifact
                state.artifacts.append(new_artifact)

            return True

        except Exception as e:
            logger.error(f"Revision execution failed: {e}")
            return False

    def _identify_steps_to_revise(
        self,
        state: TaskState,
        review_result: Dict[str, Any]
    ) -> List[Step]:
        """
        Uses heuristics to determine which steps require re-execution.

        Args:
            state (TaskState): Current state.
            review_result (Dict[str, Any]): Reviewer findings.

        Returns:
            List[Step]: Steps identified for revision.
        """
        if not state.plan:
            return []

        # Simple heuristic: revise the last completed step
        completed_steps = [
            step for step in state.plan.steps
            if getattr(step, 'status', None) == "COMPLETED"
        ]

        if completed_steps:
            return [completed_steps[-1]]

        return []

    def _extract_static_checks(self, quality_reports: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """
        Aggregates results from non-semantic checks.

        Args:
            quality_reports: Artifact reports.

        Returns:
            Dict[str, Any]: Mapping of artifact IDs to static check findings.
        """
        static_checks = {}
        for artifact_id, report in quality_reports.items():
            if "static_checks" in report:
                static_checks[artifact_id] = report["static_checks"]
        return static_checks

    def _extract_llm_checks(self, quality_reports: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """
        Aggregates results from artifact-level semantic checks.

        Args:
            quality_reports: Artifact reports.

        Returns:
            Dict[str, Any]: Mapping of artifact IDs to semantic check findings.
        """
        llm_checks = {}
        for artifact_id, report in quality_reports.items():
            if "llm_checks" in report:
                llm_checks[artifact_id] = report["llm_checks"]
        return llm_checks

    def _log_iteration_summary(self, result: Dict[str, Any]) -> None:
        """Logs high-level results of a review iteration."""
        logger.info(
            f"Review Iteration {result['iteration_count']} Summary:\n"
            f"  Overall Success: {result['overall_success']}\n"
            f"  Quality Score: {result['quality_score']:.1f}/100\n"
            f"  Needs Revision: {result['needs_revision']}\n"
            f"  Revision Instructions: {len(result.get('revision_instructions', []))}\n"
            f"  Strengths: {len(result.get('strengths', []))}\n"
            f"  Weaknesses: {len(result.get('weaknesses', []))}"
        )
