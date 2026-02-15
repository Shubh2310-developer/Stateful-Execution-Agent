from typing import Any, Dict, List, Optional
from src.core.types import Step, Artifact, Decision, UserMemory
from src.executor.tool_orchestrator import ToolOrchestrator
from src.executor.artifact_manager import ArtifactManager
from src.llm.groq_client import groq_client
from src.llm.prompt_builder import prompt_builder
from src.llm.response_parser import ResponseParser
from src.memory.retrieval.context_builder import ContextBuilder
from src.memory.short_term.working_memory import WorkingMemory
from src.utils.logger import logger
from datetime import datetime, timezone
from uuid import uuid4

class StepRunner:
    """Executes a single step from the plan, coordinating tools and state."""

    def __init__(self, artifact_manager: ArtifactManager):
        self.tool_orchestrator = ToolOrchestrator()
        self.artifact_manager = artifact_manager
        self.context_builder = ContextBuilder()

    async def run_step(
        self,
        task_id: str,
        step: Step,
        available_artifacts: List[Artifact],
        user_memory: Optional[UserMemory] = None,
        working_memory: Optional[WorkingMemory] = None
    ) -> Dict[str, Any]:
        step_id = getattr(step, 'id', getattr(step, 'step_id', 'unknown'))
        action_name = getattr(step, 'action', 'unknown')

        logger.info(f"Running step {step_id}: {action_name}")

        # 1. Prepare context for LLM
        artifact_contents = {
            art.id: self.artifact_manager.get_artifact_content(art)
            for art in available_artifacts
        }

        # Build comprehensive context using ContextBuilder
        llm_context = None
        if working_memory:
            llm_context = self.context_builder.build_context(
                task_context=working_memory.context,
                user_memory=user_memory
            )

        # Initial prompt
        messages = prompt_builder.build_executor_prompt(
            step=step,
            available_artifacts=artifact_contents,
            tool_list=self.tool_orchestrator.tool_selector.get_available_tool_names(),
            user_preferences=getattr(user_memory, 'preferences', None) if user_memory else None,
            context=llm_context,
            include_examples=True
        )

        max_retries = 3
        attempt = 0
        final_tool_output = None
        final_validation_result = None
        decisions = []
        start_execution_time = datetime.now(timezone.utc)

        while attempt < max_retries:
            attempt += 1
            logger.info(f"Step {step_id} - Attempt {attempt}/{max_retries}")

            # 2. Get tool parameters from LLM
            response_text = await groq_client.generate_response(messages)
            execution_decision = ResponseParser.parse_json_response(response_text)

            action, params = ResponseParser.extract_action_and_params(execution_decision)
            reasoning = execution_decision.get("reasoning", "Executing as planned.")
            logger.info(f"Execution Reasoning: {reasoning}")

            # 3. Invoke Tool
            try:
                tool_output = await self.tool_orchestrator.invoke_tool(
                    action,
                    params,
                    available_artifacts=available_artifacts,
                    user_memory=user_memory
                )
            except Exception as e:
                logger.error(f"Tool execution error: {str(e)}")
                tool_output = {"error": str(e)}

            final_tool_output = tool_output

            # 4. Self-Correction / Verification
            logger.info(f"Verifying output for attempt {attempt}")
            success_criteria = getattr(step, 'success_criteria', ["Output must be relevant to the step goal"])
            if isinstance(success_criteria, str):
                success_criteria = [success_criteria]

            validation_messages = prompt_builder.build_validator_prompt(
                step_description=step.description,
                success_criteria=success_criteria,
                step_output=tool_output
            )

            validation_response = await groq_client.generate_response(validation_messages)
            validation_result = ResponseParser.parse_json_response(validation_response)
            final_validation_result = validation_result

            passed = validation_result.get("passed", False)
            issues = validation_result.get("issues", [])

            # Record this decision
            decision = Decision(
                decision_id=f"dec_{uuid4().hex[:8]}",
                task_id=task_id,
                step_id=step_id,
                timestamp=datetime.now(timezone.utc),
                decision_point=f"Execution Attempt {attempt}",
                reasoning=reasoning,
                choice_made=action,
                confidence=execution_decision.get("confidence", 1.0),
                impact="medium",
                metadata={
                    "validation": validation_result,
                    "tool_params": params,
                    "attempt": attempt
                }
            )
            decisions.append(decision)

            if passed:
                logger.info(f"Step {step_id} PASSED verification on attempt {attempt}")
                break

            if attempt < max_retries:
                logger.warning(f"Step {step_id} FAILED verification. Issues: {issues}. Retrying...")
                # Update messages for correction
                messages = prompt_builder.build_correction_prompt(
                    step=step,
                    previous_action=action,
                    previous_params=params,
                    previous_output=tool_output,
                    issues=issues,
                    available_artifacts=artifact_contents,
                    tool_list=self.tool_orchestrator.tool_selector.get_available_tool_names(),
                    user_preferences=getattr(user_memory, 'preferences', None) if user_memory else None
                )

        end_execution_time = datetime.now(timezone.utc)

        # 5. Create Final Artifact
        artifact = await self.artifact_manager.create_artifact(
            task_id=task_id,
            step_id=step_id,
            artifact_type="data",
            content=final_tool_output,
            format="json",
            metadata={"validation": final_validation_result, "attempts": attempt}
        )

        return {
            "status": "completed" if final_validation_result.get("passed", False) else "failed",
            "artifact": artifact,
            "decisions": decisions,
            "duration": (end_execution_time - start_execution_time).total_seconds(),
            "validation": final_validation_result,
            "attempts": attempt
        }
