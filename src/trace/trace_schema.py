from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class TraceEntry(BaseModel):
    trace_id: str
    task_id: str
    step_id: Optional[str] = None
    decision_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    event_type: str  # planning | execution | validation | error | user_interaction
    context: Dict[str, Any]
    reasoning: Optional[Dict[str, Any]] = None
    action_taken: Optional[Dict[str, Any]] = None
    outcome: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = {}
    tags: List[str] = []

class DecisionTrace(BaseModel):
    decision_id: str
    task_id: str
    step_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    decision_point: str
    options_considered: List[Dict[str, Any]] = []
    decision_rationale: str
    confidence_score: float
    risk_assessment: str = "low"
    final_choice: str
    metadata: Dict[str, Any] = {}
    tags: List[str] = []
