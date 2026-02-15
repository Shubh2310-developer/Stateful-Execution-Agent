"""
Integration Example: Enhanced Reviewer with Workflow Engine

This example shows how to integrate the Enhanced Reviewer Module
into the main workflow engine for automatic quality assurance.
"""

from typing import Optional
from src.core.types import TaskState, TaskStatus, UserMemory
from src.reviewer.reviewer import Reviewer
from src.executor.executor import Executor
from src.planner.planner import Planner
from src.utils.logger import logger


class WorkflowEngineWithReview:
    """
    Enhanced Workflow Engine with integrated review and self-correction.

    Flow:
    1. Parse goal
    2. Generate plan
    3. Execute plan
    4. Review execution (with automatic correction loop)
    5. Update task status based on review
    6. Return final result
    """

    def __init__(self, max_review_iterations: int = 2):
        """
        Initialize workflow engine with review capability.

        Args:
            max_review_iterations: Maximum review/revision iterations (default: 2)
        """
        self.planner = Planner()
        self.executor = Executor()
        self.reviewer = Reviewer(max_iterations=max_review_iterations)

    async def execute_task_with_review(
        self,
        state: TaskState,
        user_memory: Optional[UserMemory] = None
    ) -> TaskState:
        """
        Executes a task with automatic review and quality assurance.

        Args:
            state: Initial task state
            user_memory: Optional user memory for personalization

        Returns:
            Updated task state with review results
        """
        logger.info(f"Starting task {state.task_id} with review-enabled workflow")

        try:
            # 1. Planning Phase
            if not state.plan:
                logger.info("Generating plan...")
                state = await self.planner.generate_plan(state, user_memory)

            # 2. Execution Phase
            logger.info("Executing plan...")
            state = await self.executor.execute_plan(state, user_memory)

            if state.status == TaskStatus.FAILED:
                logger.error(f"Execution failed for task {state.task_id}")
                return state

            # 3. Review Phase (with automatic correction loop)
            logger.info("Starting review with automatic correction loop...")
            review_result = await self.reviewer.review_with_correction_loop(
                state=state,
                user_memory=user_memory
            )

            # 4. Update task state based on review
            state = self._update_state_from_review(state, review_result)

            # 5. Log final outcome
            self._log_final_outcome(state, review_result)

            return state

        except Exception as e:
            logger.error(f"Workflow execution failed: {str(e)}")
            state.status = TaskStatus.FAILED
            state.metadata["error"] = str(e)
            return state

    def _update_state_from_review(
        self,
        state: TaskState,
        review_result: dict
    ) -> TaskState:
        """
        Updates task state based on review results.

        Args:
            state: Current task state
            review_result: Review result dictionary

        Returns:
            Updated task state
        """
        # Set final status
        if review_result.get("overall_success", False):
            state.status = TaskStatus.COMPLETED
            logger.info(f"Task {state.task_id} COMPLETED after review")
        else:
            # Failed review even after max iterations
            state.status = TaskStatus.FAILED
            logger.warning(
                f"Task {state.task_id} FAILED review. "
                f"Score: {review_result.get('quality_score', 0)}/100"
            )

        # Store review metadata
        state.metadata.update({
            "review": {
                "quality_score": review_result.get("quality_score", 0),
                "iteration_count": review_result.get("iteration_count", 0),
                "requirement_coverage": review_result.get("requirement_coverage", {}),
                "feedback": review_result.get("feedback", ""),
                "strengths": review_result.get("strengths", []),
                "weaknesses": review_result.get("weaknesses", []),
                "recommendations": review_result.get("recommendations", [])
            }
        })

        return state

    def _log_final_outcome(self, state: TaskState, review_result: dict) -> None:
        """Logs comprehensive final outcome."""
        quality_score = review_result.get("quality_score", 0)
        iterations = review_result.get("iteration_count", 0)
        success = review_result.get("overall_success", False)

        logger.info(
            f"\n{'='*80}\n"
            f"TASK COMPLETION SUMMARY\n"
            f"{'='*80}\n"
            f"Task ID: {state.task_id}\n"
            f"Status: {state.status.value}\n"
            f"Quality Score: {quality_score:.1f}/100\n"
            f"Review Iterations: {iterations}\n"
            f"Overall Success: {success}\n"
            f"{'='*80}"
        )

        # Log requirement coverage
        coverage = review_result.get("requirement_coverage", {})
        if coverage:
            logger.info(
                f"Requirement Coverage:\n"
                f"  Total: {coverage.get('total_requirements', 0)}\n"
                f"  Met: {coverage.get('met_requirements', 0)}\n"
                f"  Partially Met: {coverage.get('partially_met', 0)}\n"
                f"  Unmet: {coverage.get('unmet_requirements', 0)}\n"
                f"  Percentage: {coverage.get('coverage_percentage', 0)}%"
            )

        # Log feedback
        feedback = review_result.get("feedback", "")
        if feedback:
            logger.info(f"Reviewer Feedback:\n{feedback}")


# Example usage
async def example_workflow_with_review():
    """Example of using the workflow engine with review."""
    from src.core.types import Goal, TaskState

    # Create a task
    goal = Goal(
        request="Create a market analysis report for Q4 2025",
        success_criteria=[
            "Include at least 3 market segments",
            "Provide data-driven insights",
            "Include actionable recommendations",
            "Professional format and tone"
        ],
        constraints=["Maximum 10 pages", "Use recent data"]
    )

    state = TaskState(
        task_id="task_example",
        user_id="user_123",
        goal=goal,
        status=TaskStatus.PENDING
    )

    # Execute with review
    workflow = WorkflowEngineWithReview(max_review_iterations=2)
    final_state = await workflow.execute_task_with_review(state)

    print(f"\nFinal Status: {final_state.status.value}")
    print(f"Quality Score: {final_state.metadata.get('review', {}).get('quality_score', 'N/A')}")


# Integration with existing orchestration layer
async def integrate_with_orchestrator(task_id: str, user_id: str):
    """
    Example of integrating reviewer into the existing orchestration layer.

    This would be called from src/orchestration/workflow_engine.py
    """
    from src.state.state_manager import StateManager
    from src.memory.memory_manager import MemoryManager

    # Load task state
    state_manager = StateManager()
    state = await state_manager.load_state(task_id)

    # Load user memory
    memory_manager = MemoryManager()
    user_memory = await memory_manager.load_user_memory(user_id)

    # Execute with review
    workflow = WorkflowEngineWithReview(max_review_iterations=2)
    final_state = await workflow.execute_task_with_review(state, user_memory)

    # Save updated state
    await state_manager.save_state(final_state)

    return final_state


# Minimal integration for existing workflow_engine.py
def add_review_step_to_existing_workflow(workflow_engine_instance):
    """
    Shows how to add review step to existing workflow engine.

    Add this to src/orchestration/workflow_engine.py after execution:
    """
    example_code = """
    # In workflow_engine.py, after execution completes:

    from src.reviewer.reviewer import Reviewer

    # ... existing execution code ...

    # After executor.execute_plan()
    if state.status == TaskStatus.COMPLETED:
        # Run review with automatic correction
        reviewer = Reviewer(max_iterations=2)
        review_result = await reviewer.review_with_correction_loop(
            state=state,
            user_memory=user_memory
        )

        # Update status based on review
        if review_result["overall_success"]:
            state.status = TaskStatus.COMPLETED
            state.metadata["quality_score"] = review_result["quality_score"]
        else:
            state.status = TaskStatus.FAILED
            state.metadata["review_feedback"] = review_result["feedback"]

        # Store comprehensive review data
        state.metadata["review"] = {
            "quality_score": review_result["quality_score"],
            "iteration_count": review_result["iteration_count"],
            "requirement_coverage": review_result["requirement_coverage"],
            "feedback": review_result["feedback"]
        }
    """
    return example_code


if __name__ == "__main__":
    import asyncio
    print("Workflow Engine with Review Integration Example")
    print("=" * 80)
    print("\nThis example shows how to integrate the Enhanced Reviewer")
    print("into the main workflow for automatic quality assurance.")
    print("\nSee the code for integration patterns:")
    print("  1. WorkflowEngineWithReview - Complete workflow with review")
    print("  2. integrate_with_orchestrator - Integration with orchestration layer")
    print("  3. add_review_step_to_existing_workflow - Minimal integration")
    print("\n" + "=" * 80)
