from fastapi import Request
from src.trace.context import set_trace_context
from src.utils.logger import logger
import uuid

async def trace_context_middleware(request: Request, call_next):
    """
    Middleware to initialize TraceContext from request headers.
    Looks for 'X-Task-ID' and 'X-Step-ID' headers.
    """
    task_id = request.headers.get("X-Task-ID")
    step_id = request.headers.get("X-Step-ID")

    # If no task_id provided for an API call, we might generate a request-scoped ID
    # or just leave it empty depending on whether we want to trace all API calls
    # as "tasks" or only those explicitly part of an agent task.
    # For now, we'll log it if present.

    # We can also capture a correlation ID for the request itself
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))

    metadata = {
        "request_id": request_id,
        "path": request.url.path,
        "method": request.method,
        "client_host": request.client.host if request.client else None
    }

    set_trace_context(task_id=task_id, step_id=step_id, metadata=metadata)

    if task_id:
        logger.debug(f"Trace context set for request: task_id={task_id}, step_id={step_id}")

    response = await call_next(request)

    # Add request ID to response headers
    response.headers["X-Request-ID"] = request_id

    return response
