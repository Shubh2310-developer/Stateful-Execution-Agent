from typing import List, Dict, Any, Optional
from motor.motor_asyncio import AsyncIOMotorClient
from src.core.config import settings
from src.trace.trace_schema import DecisionTrace
from src.utils.logger import logger
from datetime import datetime
from uuid import uuid4

class DecisionRecorder:
    """Specifically records reasoning process and choices for learning and audit."""

    def __init__(self):
        self.client = AsyncIOMotorClient(settings.MONGODB_URL)
        self.db = self.client[settings.MONGODB_DB_NAME]
        self.collection = self.db.decisions

    async def record_decision(
        self,
        task_id: str,
        decision_point: str,
        rationale: str,
        final_choice: str,
        options_considered: List[Dict[str, Any]] = None,
        confidence_score: float = 1.0,
        risk_assessment: str = "low",
        step_id: Optional[str] = None
    ) -> str:
        decision_id = f"dec_{uuid4().hex[:8]}"
        trace = DecisionTrace(
            decision_id=decision_id,
            task_id=task_id,
            step_id=step_id,
            timestamp=datetime.utcnow(),
            decision_point=decision_point,
            options_considered=options_considered or [],
            decision_rationale=rationale,
            confidence_score=confidence_score,
            risk_assessment=risk_assessment,
            final_choice=final_choice
        )

        try:
            await self.collection.insert_one(trace.dict())
            logger.info(f"Decision recorded: {decision_id} - {decision_point}")
            return decision_id
        except Exception as e:
            logger.error(f"Failed to record decision: {str(e)}")
            return ""

decision_recorder = DecisionRecorder()
