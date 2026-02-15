from typing import List, Dict, Any, Optional
from motor.motor_asyncio import AsyncIOMotorClient
from src.core.config import settings
from src.trace.trace_schema import TraceEntry, DecisionTrace
from src.utils.logger import logger
from datetime import datetime

class TraceQueryEngine:
    """Provides advanced querying capabilities for the decision trace log."""

    def __init__(self):
        self.client = AsyncIOMotorClient(settings.database.mongodb_uri)
        self.db = self.client[settings.database.mongodb_db]
        self.trace_collection = self.db.trace
        self.decision_collection = self.db.decisions

    async def query_traces(
        self,
        task_id: Optional[str] = None,
        event_type: Optional[str] = None,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
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
        cursor = self.trace_collection.find(query).sort("timestamp", 1).limit(limit)

        results = []
        async for doc in cursor:
            results.append(TraceEntry(**doc))

        return results

    async def get_step_trace(self, task_id: str, step_id: str) -> List[TraceEntry]:
        """Retrieves all trace entries associated with a specific plan step."""
        cursor = self.trace_collection.find({"task_id": task_id, "step_id": step_id}).sort("timestamp", 1)
        results = []
        async for doc in cursor:
            results.append(TraceEntry(**doc))
        return results

    async def get_low_confidence_decisions(self, threshold: float = 0.5, limit: int = 50) -> List[DecisionTrace]:
        """Retrieves decisions where confidence score is below the threshold."""
        query = {"confidence_score": {"$lt": threshold}}
        cursor = self.decision_collection.find(query).sort("timestamp", -1).limit(limit)

        results = []
        async for doc in cursor:
            results.append(DecisionTrace(**doc))
        return results

    async def get_decisions_by_task(self, task_id: str) -> List[DecisionTrace]:
        """Retrieves all decisions made for a specific task."""
        cursor = self.decision_collection.find({"task_id": task_id}).sort("timestamp", 1)
        results = []
        async for doc in cursor:
            results.append(DecisionTrace(**doc))
        return results

    async def search_reasoning(self, keyword: str, limit: int = 50) -> List[DecisionTrace]:
        """Full-text search within decision rationale."""
        # Note: This requires a text index on 'decision_rationale' in MongoDB
        # For now, we'll use a regex search which is slower but works without index setup
        query = {"decision_rationale": {"$regex": keyword, "$options": "i"}}
        cursor = self.decision_collection.find(query).sort("timestamp", -1).limit(limit)

        results = []
        async for doc in cursor:
            results.append(DecisionTrace(**doc))
        return results
