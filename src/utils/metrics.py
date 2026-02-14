from prometheus_client import Counter, Histogram, Gauge
import time

# Metrics definitions
TASK_CREATION_COUNT = Counter("agent_task_creation_total", "Total number of tasks created")
TASK_COMPLETION_COUNT = Counter("agent_task_completion_total", "Total number of tasks completed")
STEP_EXECUTION_DURATION = Histogram("agent_step_execution_seconds", "Time spent executing individual steps")
LLM_TOKEN_USAGE = Counter("agent_llm_token_usage_total", "Total tokens consumed", ["model", "type"])
ACTIVE_SESSIONS = Gauge("agent_active_sessions", "Number of currently active task sessions")

class MetricsTracker:
    @staticmethod
    def track_task_created():
        TASK_CREATION_COUNT.inc()

    @staticmethod
    def track_task_completed():
        TASK_COMPLETION_COUNT.inc()

    @staticmethod
    def track_step_duration(duration: float):
        STEP_EXECUTION_DURATION.observe(duration)

    @staticmethod
    def track_token_usage(model: str, usage_type: str, count: int):
        LLM_TOKEN_USAGE.labels(model=model, type=usage_type).inc(count)

    @staticmethod
    def update_active_sessions(count: int):
        ACTIVE_SESSIONS.set(count)
