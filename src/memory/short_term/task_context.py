from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from src.core.types import StepLog

class TaskContext(BaseModel):
    """Represents the immediate context and working memory for a specific task."""
    task_id: str
    active_step: Optional[str] = None
    completed_steps: List[str] = []
    step_logs: List[StepLog] = []
    working_variables: Dict[str, Any] = {}
    temporary_notes: List[str] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def add_step_log(self, step_id: str, action: str, description: str, output: Any = None):
        log = StepLog(
            step_id=step_id,
            action=action,
            description=description,
            output=output
        )
        self.step_logs.append(log)
        self.updated_at = datetime.utcnow()

    def update_variable(self, key: str, value: Any):
        self.working_variables[key] = value
        self.updated_at = datetime.utcnow()

    def add_note(self, note: str):
        self.temporary_notes.append(note)
        self.updated_at = datetime.utcnow()
