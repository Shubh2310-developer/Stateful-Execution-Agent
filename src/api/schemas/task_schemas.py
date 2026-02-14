from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from src.core.types import Plan, Artifact, Decision

class TaskCreate(BaseModel):
    user_id: str
    goal: str
    context: Optional[Dict[str, Any]] = None
    execution_mode: str = "autonomous"

class TaskUpdate(BaseModel):
    user_input: Optional[str] = None
    mode: str = "resume"  # resume | modify_plan | restart

class TaskResponse(BaseModel):
    task_id: str
    status: str
    goal_summary: str
    progress_percentage: float
    current_step: Optional[str] = None
    message: Optional[str] = None

class TaskStatusResponse(BaseModel):
    task_id: str
    status: str
    progress: Dict[str, Any]
    artifacts_produced: int
    last_activity: str
