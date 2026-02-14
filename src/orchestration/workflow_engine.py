from typing import Any, Dict, List, Optional
from src.core.types import TaskState, Plan, TaskStatus
from src.planner.planner import Planner
from src.executor.executor import Executor
from src.memory.learning.adaptation_engine import AdaptationEngine
from src.utils.logger import logger

class WorkflowEngine:
    """High-level engine that coordinates planning and execution flows."""

    def __init__(self):
        self.planner = Planner()
        self.executor = Executor()
        self.adaptation_engine = AdaptationEngine()

    async def process_task(self, state: TaskState, available_tools: List[str], user_memory: Any = None) -> TaskState:
        logger.info(f"Processing task {state.task_id} in status: {state.status}")

        # 1. Planning phase if needed
        if state.status == TaskStatus.PENDING or not state.plan:
            state.status = TaskStatus.PLANNING
            state.plan = await self.planner.create_plan(
                raw_goal=state.goal.request,
                available_tools=available_tools,
                user_memory=user_memory,
                context={"task_id": state.task_id}
            )
            state.status = TaskStatus.EXECUTING

        # 2. Execution phase
        if state.status in [TaskStatus.EXECUTING, TaskStatus.PAUSED]:
            state = await self.executor.execute_plan(state, user_memory=user_memory)

        # 3. Learning phase (Trigger loop after completion or failure)
        if state.status in [TaskStatus.COMPLETED, TaskStatus.FAILED]:
            logger.info(f"Task {state.task_id} finalized with status {state.status}. Triggering learning loop.")
            try:
                # We pass the state to the adaptation engine to extract lessons
                # Feedback can be added here if available in state.metadata
                feedback = state.metadata.get("user_feedback")
                await self.adaptation_engine.learn_from_task(state, feedback=feedback)
            except Exception as e:
                logger.error(f"Failed to run learning loop for task {state.task_id}: {str(e)}")

        return state
