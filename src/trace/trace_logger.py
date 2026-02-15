from typing import Any, Dict, Optional
from motor.motor_asyncio import AsyncIOMotorClient
from src.core.config import settings
from src.trace.trace_schema import TraceEntry
from src.trace.buffer import AsyncTraceBuffer
from src.utils.logger import logger
from datetime import datetime
from uuid import uuid4

from src.state.persistence.database_adapter import DatabaseAdapter
from src.trace.context import get_task_id, get_step_id
from datetime import datetime, timezone

class TraceLogger:
    """Logs detailed execution events and context for auditability."""

    def __init__(self, db_adapter: Optional[DatabaseAdapter] = None):
        if db_adapter:
            self.db = db_adapter.db
        else:
            self.client = AsyncIOMotorClient(settings.database.mongodb_uri)
            self.db = self.client[settings.database.mongodb_db]
        self.collection = self.db.trace
        self.buffer = AsyncTraceBuffer(self.collection)

    async def log_event(
        self,
        event_type: str,
        context: Dict[str, Any],
        task_id: Optional[str] = None,
        step_id: Optional[str] = None,
        reasoning: Optional[Dict[str, Any]] = None,
        action_taken: Optional[Dict[str, Any]] = None,
        outcome: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        resolved_task_id = task_id or get_task_id()
        resolved_step_id = step_id or get_step_id()

        if not resolved_task_id:
             # It's possible to log system events without a task, but worth noting
             if event_type not in ["system_startup", "health_check"]:
                 # logger.debug(f"Event logged without task_id: {event_type}")
                 pass
             resolved_task_id = "system"

        trace_id = f"trace_{uuid4().hex[:8]}"
        entry = TraceEntry(
            trace_id=trace_id,
            task_id=resolved_task_id,
            step_id=resolved_step_id,
            event_type=event_type,
            timestamp=datetime.now(timezone.utc),
            context=context,
            reasoning=reasoning,
            action_taken=action_taken,
            outcome=outcome,
            metadata=metadata or {}
        )

        try:
            await self.buffer.add(entry.model_dump())
            return trace_id
        except Exception as e:
            logger.error(f"Failed to log trace entry: {str(e)}")
            return ""

trace_logger = TraceLogger()
