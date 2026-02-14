from typing import List, Optional
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from src.core.config import settings
from src.state.state_schema import TaskStateSchema
from src.utils.logger import logger

class VersionManager:
    """Manages snapshots and history of task states for rollback and auditing."""

    def __init__(self):
        self.client = AsyncIOMotorClient(settings.MONGODB_URL)
        self.db = self.client[settings.MONGODB_DB_NAME]
        self.collection = self.db.state_history

    async def create_snapshot(self, state: TaskStateSchema) -> bool:
        logger.debug(f"Creating snapshot for task {state.task_id} (index: {state.current_step_index})")
        try:
            snapshot = state.dict()
            snapshot["snapshot_at"] = datetime.utcnow()
            await self.collection.insert_one(snapshot)
            return True
        except Exception as e:
            logger.error(f"Failed to create state snapshot: {str(e)}")
            return False

    async def get_history(self, task_id: str) -> List[TaskStateSchema]:
        logger.debug(f"Retrieving history for task {task_id}")
        cursor = self.collection.find({"task_id": task_id}).sort("snapshot_at", -1)
        history = []
        async for doc in cursor:
            history.append(TaskStateSchema(**doc))
        return history

    async def rollback(self, task_id: str, to_index: int) -> Optional[TaskStateSchema]:
        """Rolls back the task state to a specific step index."""
        logger.info(f"Rolling back task {task_id} to step index {to_index}")
        doc = await self.collection.find_one(
            {"task_id": task_id, "current_step_index": to_index},
            sort=[("snapshot_at", -1)]
        )
        if doc:
            return TaskStateSchema(**doc)
        return None
