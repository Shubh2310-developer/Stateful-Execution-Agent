from typing import Dict, Optional, Any
from src.state.state_manager import StateManager
from src.state.version_manager import VersionManager
from src.utils.logger import logger

class SessionManager:
    """Manages active task sessions and their lifecycle."""

    def __init__(self):
        from src.state.persistence.database_adapter import DatabaseAdapter
        db_adapter = DatabaseAdapter()
        self.state_manager = StateManager(db_adapter=db_adapter)
        self.version_manager = VersionManager(db_adapter=db_adapter)
        self._active_sessions: Dict[str, Any] = {}

    async def create_session(self, task_id: str, user_id: str, goal: Dict[str, Any]):
        logger.info(f"Creating session for task {task_id}")
        state = await self.state_manager.initialize_state(task_id, user_id, goal)
        self._active_sessions[task_id] = state
        return state

    async def get_session(self, task_id: str):
        if task_id in self._active_sessions:
            return self._active_sessions[task_id]

        state = await self.state_manager.get_state(task_id)
        if state:
            self._active_sessions[task_id] = state
            return state
        return None

    async def close_session(self, task_id: str):
        logger.info(f"Closing session for task {task_id}")
        if task_id in self._active_sessions:
            state = self._active_sessions.pop(task_id)
            await self.state_manager.save_state(state)
            await self.version_manager.create_snapshot(state)
