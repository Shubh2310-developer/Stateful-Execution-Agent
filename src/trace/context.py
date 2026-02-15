from contextvars import ContextVar
from typing import Optional, Dict, Any
from dataclasses import dataclass, field

@dataclass
class TraceContext:
    task_id: Optional[str] = None
    step_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

_trace_context_var: ContextVar[TraceContext] = ContextVar("trace_context", default=TraceContext())

def get_current_context() -> TraceContext:
    return _trace_context_var.get()

def set_trace_context(task_id: str, step_id: Optional[str] = None, metadata: Dict[str, Any] = None):
    ctx = TraceContext(task_id=task_id, step_id=step_id, metadata=metadata or {})
    _trace_context_var.set(ctx)

def get_task_id() -> Optional[str]:
    return get_current_context().task_id

def get_step_id() -> Optional[str]:
    return get_current_context().step_id
