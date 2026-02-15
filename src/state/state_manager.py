import hashlib
import json
from typing import Any, Dict, Optional, List
from src.state.state_schema import TaskStateSchema
from src.state.persistence.database_adapter import DatabaseAdapter
from src.core.types import Goal, TaskStatus
from src.utils.logger import logger
from datetime import datetime, timezone

class StateManager:
    """Manages the lifecycle and transitions of task states."""

    def __init__(self, db_adapter: Optional[DatabaseAdapter] = None):
        self.persistence = db_adapter or DatabaseAdapter()

    def _calculate_checksum(self, state: TaskStateSchema) -> str:
        """Calculates SHA-256 checksum of the state content."""
        # Exclude updated_at and checksum itself from calculation
        state_dict = state.dict(exclude={"updated_at", "checksum"})
        state_json = json.dumps(state_dict, sort_keys=True, default=str)
        return hashlib.sha256(state_json.encode()).hexdigest()

    async def get_state(self, task_id: str) -> Optional[TaskStateSchema]:
        state = await self.persistence.load_state(task_id)
        if state and state.checksum:
            # Verify integrity
            current_checksum = self._calculate_checksum(state)
            if current_checksum != state.checksum:
                logger.warning(f"State checksum mismatch for task {task_id}! Potential corruption.")
        return state

    async def save_state(self, task_id: str, state: TaskStateSchema, is_milestone: bool = False, summary: Optional[str] = None) -> bool:
        """Saves state with checksumming and version increment."""
        state.updated_at = datetime.now(timezone.utc)
        state.checksum = self._calculate_checksum(state)

        # DatabaseAdapter.save_state handles version_counter increment via $inc
        success = await self.persistence.save_state(state, is_milestone=is_milestone, summary=summary)

        if success:
            # Sync the local version counter if it was incremented in DB
            # find_one_and_update in adapter returns the doc with incremented version
            # but we'd need to fetch it or have save_state return it.
            # For now, we assume the increment happened correctly.
            pass
        return success

    async def initialize_state(self, task_id: str, user_id: str, goal_data: Dict[str, Any]) -> TaskStateSchema:
        logger.info(f"Initializing new state for task {task_id}")

        if isinstance(goal_data, dict):
            goal = Goal(**goal_data)
        else:
            goal = goal_data

        state = TaskStateSchema(
            task_id=task_id,
            user_id=user_id,
            goal=goal,
            status=TaskStatus.PENDING,
            version_counter=1
        )
        state.checksum = self._calculate_checksum(state)
        await self.save_state(task_id, state, is_milestone=True, summary="Task initialization")
        return state

    async def update_status(self, task_id: str, status: TaskStatus) -> bool:
        state = await self.get_state(task_id)
        if state:
            state.status = status
            return await self.save_state(task_id, state)
        return False

    async def add_artifact(self, task_id: str, artifact: Any) -> bool:
        """Adds an artifact reference to the task state."""
        state = await self.get_state(task_id)
        if state:
            state.artifacts.append(artifact)
            # Significant update, potentially a milestone
            return await self.save_state(task_id, state, is_milestone=True, summary=f"Added artifact: {artifact.id}")
        return False
