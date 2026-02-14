from typing import Any, Dict, Optional, List
from motor.motor_asyncio import AsyncIOMotorClient
from src.core.config import settings
from src.core.types import UserMemory, HistoricalPattern, UserProfile, UserPreferences
from src.utils.logger import logger
from datetime import datetime

class MemoryManager:
    """Manages retrieval and storage of short-term and long-term memory."""

    def __init__(self):
        self.client = AsyncIOMotorClient(settings.database.mongodb_uri)
        self.db = self.client[settings.database.mongodb_db]
        self.profiles = self.db.user_profiles
        self.patterns = self.db.historical_patterns

    async def get_user_memory(self, user_id: str) -> Optional[UserMemory]:
        """Retrieves profile and preferences for a user."""
        logger.debug(f"Retrieving memory for user: {user_id}")
        doc = await self.profiles.find_one({"user_id": user_id})
        if doc:
            return UserMemory(**doc)
        return None

    async def save_user_memory(self, memory: UserMemory) -> bool:
        """Saves or updates user profile and preferences."""
        logger.debug(f"Saving memory for user: {memory.user_id}")
        try:
            memory.last_updated = datetime.utcnow()
            # Convert to dict and handle nested Pydantic models
            memory_dict = memory.dict()
            await self.profiles.update_one(
                {"user_id": memory.user_id},
                {"$set": memory_dict},
                upsert=True
            )
            return True
        except Exception as e:
            logger.error(f"Failed to save user memory: {str(e)}")
            return False

    async def update_user_preferences(self, user_id: str, updates: Dict[str, Any]) -> bool:
        """Partial update of user preferences."""
        logger.info(f"Updating preferences for user: {user_id}")
        try:
            # Flatten the updates to use dot notation for nested preference fields
            flat_updates = {}
            for k, v in updates.items():
                flat_updates[f"preferences.{k}"] = v

            flat_updates["last_updated"] = datetime.utcnow()

            await self.profiles.update_one(
                {"user_id": user_id},
                {"$set": flat_updates}
            )
            return True
        except Exception as e:
            logger.error(f"Failed to update user preferences: {str(e)}")
            return False

    async def add_historical_pattern(self, pattern: HistoricalPattern) -> bool:
        """Saves a new historical pattern for a user."""
        logger.info(f"Adding new historical pattern for user: {pattern.user_id}")
        try:
            await self.patterns.insert_one(pattern.dict())
            return True
        except Exception as e:
            logger.error(f"Failed to add historical pattern: {str(e)}")
            return False

    async def search_patterns(self, user_id: str, query_vector: List[float], limit: int = 3) -> List[HistoricalPattern]:
        """
        Retrieves relevant historical patterns using vector search.
        Note: Requires Atlas Vector Search index on 'embedding' field.
        """
        logger.debug(f"Searching historical patterns for user: {user_id}")
        try:
            # Basic implementation - real hybrid search would use aggregation with $vectorSearch
            pipeline = [
                {
                    "$search": {
                        "index": "vector_index",
                        "knnBeta": {
                            "vector": query_vector,
                            "path": "embedding",
                            "k": limit,
                            "filter": {"user_id": {"$eq": user_id}}
                        }
                    }
                }
            ]

            # Since local MongoDB might not have Atlas Search, we might need a fallback
            # or use a standard find if vector search isn't available.
            # For this implementation, we'll assume the retrieval engine handles the vector math
            # if we are in a non-Atlas environment, or we use the aggregate pipeline.

            cursor = self.patterns.aggregate(pipeline)
            results = []
            async for doc in cursor:
                results.append(HistoricalPattern(**doc))
            return results
        except Exception as e:
            logger.error(f"Pattern search failed: {str(e)}")
            return []
