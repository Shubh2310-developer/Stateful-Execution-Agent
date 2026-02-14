from typing import Any, Dict, List, Optional
from pydantic import BaseModel
from datetime import datetime

class TraceEntryResponse(BaseModel):
    trace_id: str
    task_id: str
    step_id: Optional[str] = None
    event_type: str
    timestamp: datetime
    context: Dict[str, Any]
    outcome: Optional[Dict[str, Any]] = None

class TraceSummary(BaseModel):
    task_id: str
    total_entries: int
    entries: List[TraceEntryResponse]
