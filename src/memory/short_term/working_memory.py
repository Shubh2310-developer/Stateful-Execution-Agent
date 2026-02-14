from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from src.memory.short_term.task_context import TaskContext
from src.utils.logger import logger

class WorkingMemory:
    """Manages active, in-memory state and variables during execution."""

    def __init__(self, task_id: str):
        self.context = TaskContext(task_id=task_id)

    def set(self, key: str, value: Any):
        self.context.update_variable(key, value)

    def get(self, key: str, default: Any = None) -> Any:
        return self.context.working_variables.get(key, default)

    def add_observation(self, note: str):
        self.context.add_note(note)

    def get_full_context(self) -> Dict[str, Any]:
        return self.context.dict()
