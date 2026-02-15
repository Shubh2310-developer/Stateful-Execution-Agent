from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
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

class ProgressInfo(BaseModel):
    completed_steps: int
    total_steps: int
    percentage: float
    current_step: Optional[str] = None

class TaskStatusResponse(BaseModel):
    task_id: str
    status: str
    progress: ProgressInfo
    artifacts_produced: int
    last_activity: str


# Feedback Schemas
class FeedbackSubmission(BaseModel):
    """Request schema for submitting user feedback."""
    rating: int = Field(ge=1, le=5, description="Rating on 1-5 scale")
    text_feedback: Optional[str] = Field(None, description="Optional text feedback")


class PreferenceUpdateResponse(BaseModel):
    """Response schema for a single preference update."""
    field: str
    old_value: Any
    new_value: Any
    confidence: float
    reasoning: Optional[str] = None


class FeedbackInsightResponse(BaseModel):
    """Response schema for an actionable insight."""
    insight: str
    confidence: float
    action: str
    category: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


class FeedbackResponse(BaseModel):
    """Response schema for processed feedback."""
    feedback_id: str
    processed_at: str
    sentiment: str
    categories: List[str]
    correlations: Dict[str, Dict[str, float]] = Field(default_factory=dict)
    preference_updates: List[PreferenceUpdateResponse] = Field(default_factory=list)
    historical_pattern_updated: bool
    insights: List[FeedbackInsightResponse] = Field(default_factory=list)
    recommendations_for_future: List[str] = Field(default_factory=list)
