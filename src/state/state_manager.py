from typing import Any, Dict, Optional, List
from src.state.state_schema import TaskStateSchema
from src.state.persistence.database_adapter import DatabaseAdapter
from src.utils.logger import logger
from datetime import datetime

class StateManager:
    """Manages the lifecycle and transitions of task states."""

    def __init__(self):
        self.persistence = DatabaseAdapter()

    async def get_state(self, task_id: str) -> Optional[TaskStateSchema]:
        return await self.persistence.load_state(task_id)

    async def save_state(self, state: TaskStateSchema) -> bool:
        state.updated_at = datetime.utcnow()
        return await self.persistence.save_state(state)

    async def initialize_state(self, task_id: str, user_id: str, goal: Dict[str, Any]) -> TaskStateSchema:
        logger.info(f"Initializing new state for task {task_id}")
        state = TaskStateSchema(
            task_id=task_id,
            user_id=user_id,
            goal=goal,
            status="pending"
        )
        await self.save_state(state)
        return state

    async def update_status(self, task_id: str, status: str) -> bool:
        state = await self.get_state(task_id)
        if state:
            state.status = status
            return await self.save_state(state)
        return False
