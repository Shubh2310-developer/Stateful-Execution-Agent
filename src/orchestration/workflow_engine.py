from typing import Any, Dict, List, Optional
from src.core.types import TaskState, Plan, TaskStatus
from src.planner.planner import Planner
from src.executor.executor import Executor
from src.reviewer.reviewer import Reviewer
from src.state.state_manager import StateManager
from src.memory.memory_manager import MemoryManager
from src.memory.learning.adaptation_engine import AdaptationEngine
from src.trace.trace_logger import trace_logger
from src.trace.decision_recorder import decision_recorder
from src.utils.logger import logger

class WorkflowEngine:
    """High-level engine that coordinates planning and execution flows."""

    def __init__(self):
        self.planner = Planner()
        self.executor = Executor()
        self.reviewer = Reviewer()
        self.state_manager = StateManager()
        self.memory_manager = MemoryManager()
        self.adaptation_engine = AdaptationEngine()

    async def process_task(self, state: TaskState, available_tools: List[str], user_memory: Any = None) -> TaskState:
        logger.info(f"Processing task {state.task_id} in status: {state.status}")
        
        # Helper function to safely get status value (handles both enum and string)
        def get_status_value(status):
            return status.value if hasattr(status, 'value') else str(status)
        
        # Log workflow start
        await trace_logger.log_event(
            event_type="workflow_start",
            context={"task_id": state.task_id, "status": get_status_value(state.status)},
            task_id=state.task_id,
            metadata={"available_tools": available_tools}
        )

        # 1. Planning phase if needed
        if state.status in [TaskStatus.PENDING, TaskStatus.PLANNING] or not state.plan:
            state.status = TaskStatus.PLANNING
            await trace_logger.log_event(
                event_type="planning_start",
                context={"goal": state.goal.request},
                task_id=state.task_id
            )
            
            state.plan = await self.planner.create_plan(
                raw_goal=state.goal.request,
                available_tools=available_tools,
                user_memory=user_memory,
                context={"task_id": state.task_id}
            )
            
            await trace_logger.log_event(
                event_type="planning_complete",
                context={"step_count": len(state.plan.steps)},
                task_id=state.task_id,
                outcome={"plan_id": state.plan.task_id}
            )
            
            state.status = TaskStatus.EXECUTING
            # Persist state after planning
            await self.state_manager.save_state(state.task_id, state)

        # 2. Execution phase
        if state.status in [TaskStatus.EXECUTING, TaskStatus.PAUSED]:
            await trace_logger.log_event(
                event_type="execution_start",
                context={"step_count": len(state.plan.steps), "current_step": state.current_step_index},
                task_id=state.task_id
            )
            
            state = await self.executor.execute_plan(state, user_memory=user_memory)
            
            await trace_logger.log_event(
                event_type="execution_complete",
                context={"final_status": get_status_value(state.status), "artifacts_count": len(state.artifacts)},
                task_id=state.task_id,
                outcome={"status": get_status_value(state.status)}
            )
            
            # Persist state after execution
            await self.state_manager.save_state(state.task_id, state)

        # 3. Review phase (if execution completed)
        if state.status == TaskStatus.COMPLETED:
            await trace_logger.log_event(
                event_type="review_start",
                context={"artifacts_count": len(state.artifacts)},
                task_id=state.task_id
            )
            
            try:
                review_result = await self.reviewer.review_task(state)
                
                await trace_logger.log_event(
                    event_type="review_complete",
                    context={"review_result": review_result.get("success", False)},
                    task_id=state.task_id,
                    outcome=review_result
                )
                
                # Update state with review results
                state.metadata["review_result"] = review_result
                await self.state_manager.save_state(state.task_id, state)
                
            except Exception as e:
                logger.error(f"Review failed for task {state.task_id}: {str(e)}")
                await trace_logger.log_event(
                    event_type="review_error",
                    context={"error": str(e)},
                    task_id=state.task_id
                )

        # 4. Learning phase (Trigger loop after completion or failure)
        if state.status in [TaskStatus.COMPLETED, TaskStatus.FAILED]:
            logger.info(f"Task {state.task_id} finalized with status {state.status}. Triggering learning loop.")
            await trace_logger.log_event(
                event_type="learning_start",
                context={"status": get_status_value(state.status)},
                task_id=state.task_id
            )
            
            try:
                # We pass the state to the adaptation engine to extract lessons
                # Feedback can be added here if available in state.metadata
                feedback = state.metadata.get("user_feedback")
                await self.adaptation_engine.learn_from_task(state, feedback=feedback)
                
                await trace_logger.log_event(
                    event_type="learning_complete",
                    context={"has_feedback": feedback is not None},
                    task_id=state.task_id
                )
            except Exception as e:
                logger.error(f"Failed to run learning loop for task {state.task_id}: {str(e)}")
                await trace_logger.log_event(
                    event_type="learning_error",
                    context={"error": str(e)},
                    task_id=state.task_id
                )

        # Log workflow completion
        await trace_logger.log_event(
            event_type="workflow_complete",
            context={"final_status": get_status_value(state.status)},
            task_id=state.task_id,
            outcome={"status": get_status_value(state.status), "artifacts": len(state.artifacts)}
        )

        return state
