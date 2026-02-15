from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from src.core.types import Plan, Artifact, Decision, Goal, TaskStatus

class TaskStateSchema(BaseModel):
    task_id: str
    user_id: str
    version_counter: int = Field(default=1)
    goal: Goal
    plan: Optional[Plan] = None
    status: TaskStatus = TaskStatus.PENDING
    current_step_index: int = 0
    current_step_id: Optional[str] = None
    artifacts: List[Artifact] = Field(default_factory=list)
    decisions: List[Decision] = Field(default_factory=list)
    logs: List[Dict[str, Any]] = Field(default_factory=list)  # Execution logs
    metadata: Dict[str, Any] = Field(default_factory=dict)
    checksum: Optional[str] = None  # SHA-256 of the state content
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
