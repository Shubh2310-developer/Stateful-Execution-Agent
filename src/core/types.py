from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    PENDING = "PENDING"
    PLANNING = "PLANNING"
    EXECUTING = "EXECUTING"
    PAUSED = "PAUSED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class Goal(BaseModel):
    request: str
    success_criteria: List[str]
    constraints: List[str] = Field(default_factory=list)


class Step(BaseModel):
    step_id: str
    order: int = 1
    action: str
    description: str
    success_criteria: Optional[str] = None
    tools: List[str] = Field(default_factory=list)
    dependencies: List[str] = Field(default_factory=list)
    status: TaskStatus = TaskStatus.PENDING
    input_data: Dict[str, Any] = Field(default_factory=dict)
    output_data: Dict[str, Any] = Field(default_factory=dict)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class StepLog(BaseModel):
    """Log of a specific step execution for history tracking."""
    step_id: str
    action: str
    description: str
    output: Optional[Any] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class Artifact(BaseModel):
    id: str
    task_id: str
    step_id: Optional[str] = None
    uri: str
    type: str  # e.g., "code", "document", "image", "data"
    checksum: Optional[str] = None  # SHA-256
    size_bytes: Optional[int] = None
    mime_type: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Decision(BaseModel):
    decision_id: str
    task_id: str
    step_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    decision_point: str
    reasoning: str
    choice_made: str
    confidence: float = 1.0
    impact: str = "low"
    metadata: Dict[str, Any] = Field(default_factory=dict)


class Plan(BaseModel):
    task_id: str
    steps: List[Step]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class TaskState(BaseModel):
    task_id: str
    user_id: str
    version_counter: int = Field(default=1)
    goal: Goal
    plan: Optional[Plan] = None
    artifacts: List[Artifact] = Field(default_factory=list)
    decisions: List[Decision] = Field(default_factory=list)
    logs: List[StepLog] = Field(default_factory=list)
    status: TaskStatus = TaskStatus.PENDING
    current_step_index: int = 0
    current_step_id: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class UserProfile(BaseModel):
    """Represents a user's identity, role, and persistent attributes."""
    user_id: str
    role: Optional[str] = None
    company: Optional[str] = None
    industry: Optional[str] = None
    communication_style: str = "professional"
    technical_depth: str = "medium"
    last_updated: datetime = Field(default_factory=datetime.utcnow)


class UserPreferences(BaseModel):
    """Stores explicit and learned user preferences."""
    document_tone: str = "professional"
    detail_level: str = "medium"
    preferred_formats: List[str] = Field(default_factory=lambda: ["markdown", "pdf"])
    formatting_rules: Dict[str, Any] = Field(default_factory=dict)


class PreferenceUpdate(BaseModel):
    """Represents a proposed update to user preferences based on feedback."""
    field: str
    old_value: Any
    new_value: Any
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class HistoricalPattern(BaseModel):
    """Structured record of a past task for semantic retrieval."""
    user_id: str
    task_id: str
    goal_request: str
    plan_summary: Optional[str] = None
    approach: Optional[str] = None
    outcome: Optional[str] = None
    success_score: float = Field(ge=0.0, le=1.0)
    tags: List[str] = Field(default_factory=list)
    embedding: Optional[List[float]] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class UserMemory(BaseModel):
    user_id: str
    profile: UserProfile
    preferences: UserPreferences
    domain_knowledge: Dict[str, Any] = Field(default_factory=dict)
    last_updated: datetime = Field(default_factory=datetime.utcnow)


class UserFeedback(BaseModel):
    """Represents raw feedback received from a user."""
    feedback_id: str
    task_id: str
    user_id: str
    rating: int = Field(ge=1, le=5)
    text_feedback: Optional[str] = None
    sentiment: str = "neutral"
    categories: List[str] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class FeedbackInsight(BaseModel):
    """Actionable insight derived from feedback analysis."""
    insight: str
    confidence: float = Field(ge=0.0, le=1.0)
    action: str
    category: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
