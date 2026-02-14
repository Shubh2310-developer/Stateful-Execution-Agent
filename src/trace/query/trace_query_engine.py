from typing import List, Dict, Any, Optional
from motor.motor_asyncio import AsyncIOMotorClient
from src.core.config import settings
from src.trace.trace_schema import TraceEntry
from src.utils.logger import logger

class TraceQueryEngine:
    """Provides advanced querying capabilities for the decision trace log."""

    def __init__(self):
        self.client = AsyncIOMotorClient(settings.database.mongodb_uri)
        self.db = self.client[settings.database.mongodb_db]
        self.collection = self.db.trace

    async def query_traces(
        self,
        task_id: Optional[str] = None,
        event_type: Optional[str] = None,
        from_date: Optional[Any] = None,
        to_date: Optional[Any] = None,
        limit: int = 100
    ) -> List[TraceEntry]:
        query = {}
        if task_id:
            query["task_id"] = task_id
        if event_type:
            query["event_type"] = event_type
        if from_date or to_date:
            query["timestamp"] = {}
            if from_date:
                query["timestamp"]["$gte"] = from_date
            if to_date:
                query["timestamp"]["$lte"] = to_date

        logger.debug(f"Querying traces with: {query}")
        cursor = self.collection.find(query).sort("timestamp", 1).limit(limit)

        results = []
        async for doc in cursor:
            results.append(TraceEntry(**doc))

        return results

    async def get_step_trace(self, task_id: str, step_id: str) -> List[TraceEntry]:
        """Retrieves all trace entries associated with a specific plan step."""
        cursor = self.collection.find({"task_id": task_id, "step_id": step_id}).sort("timestamp", 1)
        results = []
        async for doc in cursor:
            results.append(TraceEntry(**doc))
        return results
