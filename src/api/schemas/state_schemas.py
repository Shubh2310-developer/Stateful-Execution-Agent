from typing import Any, Dict, List, Optional
from pydantic import BaseModel
from datetime import datetime
from src.core.types import Plan, Artifact, Decision

class StateResponse(BaseModel):
    task_id: str
    user_id: str
    status: str
    current_step_index: int
    updated_at: datetime
    plan: Optional[Plan] = None
    artifacts: Dict[str, Artifact] = {}
    decisions: List[Decision] = []
