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
    id: str
    action: str
    description: str
    tools: List[str] = Field(default_factory=list)
    dependencies: List[str] = Field(default_factory=list)
    status: TaskStatus = TaskStatus.PENDING
    input_data: Dict[str, Any] = Field(default_factory=dict)
    output_data: Dict[str, Any] = Field(default_factory=dict)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class Artifact(BaseModel):
    id: str
    uri: str
    type: str  # e.g., "code", "document", "image", "data"
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Plan(BaseModel):
    steps: List[Step]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class TaskState(BaseModel):
    task_id: str
    goal: Goal
    plan: Optional[Plan] = None
    artifacts: List[Artifact] = Field(default_factory=list)
    status: TaskStatus = TaskStatus.PENDING
    current_step_id: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class UserMemory(BaseModel):
    user_id: str
    profile: Dict[str, Any] = Field(default_factory=dict)
    preferences: Dict[str, Any] = Field(default_factory=dict)
    domain_knowledge: Dict[str, Any] = Field(default_factory=dict)
    historical_patterns: List[Dict[str, Any]] = Field(default_factory=list)
