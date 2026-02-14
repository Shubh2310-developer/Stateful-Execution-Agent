from typing import Any, Dict, Optional
from motor.motor_asyncio import AsyncIOMotorClient
from src.core.config import settings
from src.trace.trace_schema import TraceEntry
from src.utils.logger import logger
from datetime import datetime
from uuid import uuid4

from src.state.persistence.database_adapter import DatabaseAdapter

class TraceLogger:
    """Logs detailed execution events and context for auditability."""

    def __init__(self, db_adapter: Optional[DatabaseAdapter] = None):
        if db_adapter:
            self.db = db_adapter.db
        else:
            self.client = AsyncIOMotorClient(settings.database.mongodb_uri)
            self.db = self.client[settings.database.mongodb_db]
        self.collection = self.db.trace

    async def log_event(
        self,
        task_id: str,
        event_type: str,
        context: Dict[str, Any],
        step_id: Optional[str] = None,
        reasoning: Optional[Dict[str, Any]] = None,
        action_taken: Optional[Dict[str, Any]] = None,
        outcome: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        trace_id = f"trace_{uuid4().hex[:8]}"
        entry = TraceEntry(
            trace_id=trace_id,
            task_id=task_id,
            step_id=step_id,
            event_type=event_type,
            timestamp=datetime.utcnow(),
            context=context,
            reasoning=reasoning,
            action_taken=action_taken,
            outcome=outcome,
            metadata=metadata or {}
        )

        try:
            await self.collection.insert_one(entry.dict())
            logger.debug(f"Trace logged: {trace_id} for task {task_id}")
            return trace_id
        except Exception as e:
            logger.error(f"Failed to log trace entry: {str(e)}")
            return ""

trace_logger = TraceLogger()
