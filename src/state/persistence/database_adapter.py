from typing import Any, Dict, Optional
from motor.motor_asyncio import AsyncIOMotorClient
from src.core.config import settings
from src.state.state_schema import TaskStateSchema
from src.utils.logger import logger

class DatabaseAdapter:
    """Adapter for persisting task state to MongoDB."""

    def __init__(self):
        self.client = AsyncIOMotorClient(settings.MONGODB_URL)
        self.db = self.client[settings.MONGODB_DB_NAME]
        self.collection = self.db.state

    async def save_state(self, state: TaskStateSchema) -> bool:
        logger.debug(f"Saving state for task {state.task_id} to database")
        try:
            # Upsert the state
            await self.collection.update_one(
                {"task_id": state.task_id},
                {"$set": state.dict()},
                upsert=True
            )
            return True
        except Exception as e:
            logger.error(f"Failed to save state to database: {str(e)}")
            return False

    async def load_state(self, task_id: str) -> Optional[TaskStateSchema]:
        logger.debug(f"Loading state for task {task_id} from database")
        try:
            doc = await self.collection.find_one({"task_id": task_id})
            if doc:
                return TaskStateSchema(**doc)
            return None
        except Exception as e:
            logger.error(f"Failed to load state from database: {str(e)}")
            return None

    async def delete_state(self, task_id: str) -> bool:
        logger.info(f"Deleting state for task {task_id}")
        try:
            await self.collection.delete_one({"task_id": task_id})
            return True
        except Exception as e:
            logger.error(f"Failed to delete state: {str(e)}")
            return False
