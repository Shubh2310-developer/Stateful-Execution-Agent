from typing import List, Dict, Any, Optional
from motor.motor_asyncio import AsyncIOMotorClient
from src.core.config import settings
from src.utils.logger import logger

class TraceAggregator:
    """Aggregates trace data for reporting and analytics."""

    def __init__(self):
        self.client = AsyncIOMotorClient(settings.database.mongodb_uri)
        self.db = self.client[settings.database.mongodb_db]
        self.collection = self.db.trace

    async def get_task_summary(self, task_id: str) -> Dict[str, Any]:
        """Returns a summary of events for a specific task."""
        pipeline = [
            {"$match": {"task_id": task_id}},
            {"$group": {
                "_id": "$event_type",
                "count": {"$sum": 1},
                "avg_duration": {"$avg": "$metadata.duration_ms"}
            }}
        ]

        cursor = self.collection.aggregate(pipeline)
        results = {}
        async for doc in cursor:
            results[doc["_id"]] = {
                "count": doc["count"],
                "avg_duration_ms": doc.get("avg_duration")
            }

        return results

    async def get_user_stats(self, user_id: str) -> Dict[str, Any]:
        """Aggregates stats across all tasks for a specific user."""
        # This would join with the tasks collection in a real implementation
        return {"user_id": user_id, "total_tasks": 0, "success_rate": 0.0}
