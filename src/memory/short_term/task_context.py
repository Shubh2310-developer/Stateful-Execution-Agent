from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class TaskContext(BaseModel):
    """Represents the immediate context and working memory for a specific task."""
    task_id: str
    active_step: Optional[str] = None
    completed_steps: List[str] = []
    working_variables: Dict[str, Any] = {}
    temporary_notes: List[str] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def update_variable(self, key: str, value: Any):
        self.working_variables[key] = value
        self.updated_at = datetime.utcnow()

    def add_note(self, note: str):
        self.temporary_notes.append(note)
        self.updated_at = datetime.utcnow()
