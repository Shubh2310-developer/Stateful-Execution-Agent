from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from src.core.types import Plan, Artifact, Decision

class TaskStateSchema(BaseModel):
    state_version: str = "1.0"
    task_id: str
    user_id: str
    status: str = "pending"
    goal: Dict[str, Any]
    plan: Optional[Plan] = None
    current_step_index: int = 0
    artifacts: Dict[str, Artifact] = {}
    decisions: List[Decision] = []
    metadata: Dict[str, Any] = {
        "total_llm_calls": 0,
        "total_tokens_consumed": 0,
        "estimated_cost_usd": 0.0
    }
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
