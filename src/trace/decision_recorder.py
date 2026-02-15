from typing import List, Dict, Any, Optional
from motor.motor_asyncio import AsyncIOMotorClient
from src.core.config import settings
from src.trace.trace_schema import DecisionTrace
from src.trace.buffer import AsyncTraceBuffer
from src.utils.logger import logger
from datetime import datetime
from uuid import uuid4

from src.state.persistence.database_adapter import DatabaseAdapter
from src.trace.context import get_task_id, get_step_id
from datetime import datetime, timezone

class DecisionRecorder:
    """Specifically records reasoning process and choices for learning and audit."""

    def __init__(self, db_adapter: Optional[DatabaseAdapter] = None):
        if db_adapter:
            self.db = db_adapter.db
        else:
            self.client = AsyncIOMotorClient(settings.database.mongodb_uri)
            self.db = self.client[settings.database.mongodb_db]
        self.collection = self.db.decisions
        self.buffer = AsyncTraceBuffer(self.collection)

    async def record_decision(
        self,
        decision_point: str,
        rationale: str,
        final_choice: str,
        task_id: Optional[str] = None,
        options_considered: List[Dict[str, Any]] = None,
        confidence_score: float = 1.0,
        risk_assessment: str = "low",
        step_id: Optional[str] = None,
        metadata: Dict[str, Any] = None,
        tags: List[str] = None
    ) -> str:
        # Resolve task_id and step_id from context if not provided
        resolved_task_id = task_id or get_task_id()
        resolved_step_id = step_id or get_step_id()

        if not resolved_task_id:
             logger.warning(f"Decision recorded without task_id: {decision_point}")
             resolved_task_id = "unknown"

        decision_id = f"dec_{uuid4().hex[:8]}"
        trace = DecisionTrace(
            decision_id=decision_id,
            task_id=resolved_task_id,
            step_id=resolved_step_id,
            timestamp=datetime.now(timezone.utc),
            decision_point=decision_point,
            options_considered=options_considered or [],
            decision_rationale=rationale,
            confidence_score=confidence_score,
            risk_assessment=risk_assessment,
            final_choice=final_choice,
            metadata=metadata or {},
            tags=tags or []
        )

        try:
            await self.buffer.add(trace.model_dump())
            return decision_id
        except Exception as e:
            logger.error(f"Failed to record decision: {str(e)}")
            return ""

decision_recorder = DecisionRecorder()
