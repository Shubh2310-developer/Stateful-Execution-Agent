import functools
import time
import inspect
from typing import Callable, Any, Optional, Dict
from src.trace.trace_logger import trace_logger
from src.trace.context import get_task_id

def traced_decision(
    event_type: str = "function_execution",
    log_inputs: bool = True,
    log_outputs: bool = True
):
    """
    Decorator to automatically log function execution to the trace system.
    Captures inputs, outputs, execution time, and any exceptions.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()

            # Capture inputs if requested
            inputs = {}
            if log_inputs:
                # Map args to their names
                sig = inspect.signature(func)
                bound_args = sig.bind(*args, **kwargs)
                bound_args.apply_defaults()
                inputs = {k: str(v) for k, v in bound_args.arguments.items() if k != 'self'}

            error = None
            result = None

            try:
                if inspect.iscoroutinefunction(func):
                    result = await func(*args, **kwargs)
                else:
                    result = func(*args, **kwargs)
                return result
            except Exception as e:
                error = str(e)
                raise
            finally:
                duration = time.time() - start_time

                outcome = {
                    "status": "success" if error is None else "error",
                    "duration_ms": duration * 1000
                }

                if error:
                    outcome["error"] = error
                elif log_outputs:
                    # Be careful with large outputs
                    outcome["result"] = str(result)[:1000] if result else None

                # We fire and forget the log to not block execution
                # Note: trace_logger.log_event is async, so we need to schedule it
                # If we are in an async context, we can await it or create a task
                try:
                    import asyncio
                    context_data = {
                        "function": func.__name__,
                        "module": func.__module__,
                        "inputs": inputs
                    }

                    # Create a task for logging so we don't block the return
                    asyncio.create_task(
                        trace_logger.log_event(
                            event_type=event_type,
                            context=context_data,
                            outcome=outcome,
                            metadata={"automated_trace": True}
                        )
                    )
                except Exception as log_err:
                    # Fallback or silence logging errors to not break application logic
                    print(f"Failed to auto-log trace: {log_err}")

        return wrapper
    return decorator
