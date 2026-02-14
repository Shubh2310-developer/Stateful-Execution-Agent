from typing import Any, Dict, List
from src.core.types import TaskState, Plan
from src.planner.planner import Planner
from src.executor.executor import Executor
from src.utils.logger import logger

class WorkflowEngine:
    """High-level engine that coordinates planning and execution flows."""

    def __init__(self):
        self.planner = Planner()
        self.executor = Executor()

    async def process_task(self, state: TaskState, available_tools: List[str], user_memory: Any = None) -> TaskState:
        logger.info(f"Processing task {state.task_id} in status: {state.status}")

        # 1. Planning phase if needed
        if state.status == "pending" or not state.plan:
            state.status = "planning"
            state.plan = await self.planner.create_plan(
                raw_goal=state.goal.get("request", ""),
                available_tools=available_tools,
                user_memory=user_memory
            )
            state.status = "planned"

        # 2. Execution phase
        if state.status in ["planned", "paused"]:
            state = await self.executor.execute_plan(state, user_memory=user_memory)

        return state
