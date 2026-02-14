from typing import Any, Dict, Optional, List
from motor.motor_asyncio import AsyncIOMotorClient
from src.core.config import settings
from src.core.types import UserMemory
from src.utils.logger import logger
from datetime import datetime

class MemoryManager:
    """Manages retrieval and storage of short-term and long-term memory."""

    def __init__(self):
        self.client = AsyncIOMotorClient(settings.MONGODB_URL)
        self.db = self.client[settings.MONGODB_DB_NAME]
        self.collection = self.db.memory

    async def get_user_memory(self, user_id: str) -> Optional[UserMemory]:
        logger.debug(f"Retrieving memory for user: {user_id}")
        doc = await self.collection.find_one({"user_id": user_id})
        if doc:
            return UserMemory(**doc)
        return None

    async def save_user_memory(self, memory: UserMemory) -> bool:
        logger.debug(f"Saving memory for user: {memory.user_id}")
        try:
            memory.last_updated = datetime.utcnow()
            await self.collection.update_one(
                {"user_id": memory.user_id},
                {"$set": memory.dict()},
                upsert=True
            )
            return True
        except Exception as e:
            logger.error(f"Failed to save user memory: {str(e)}")
            return False

    async def add_historical_pattern(self, user_id: str, pattern: Dict[str, Any]) -> bool:
        logger.info(f"Adding new historical pattern for user: {user_id}")
        try:
            await self.collection.update_one(
                {"user_id": user_id},
                {"$push": {"historical_patterns": pattern}, "$set": {"last_updated": datetime.utcnow()}}
            )
            return True
        except Exception as e:
            logger.error(f"Failed to add historical pattern: {str(e)}")
            return False
