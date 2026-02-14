import uuid
import shortuuid

def generate_task_id() -> str:
    return f"task_{shortuuid.uuid()[:8]}"

def generate_step_id() -> str:
    return f"step_{shortuuid.uuid()[:8]}"

def generate_artifact_id() -> str:
    return f"art_{shortuuid.uuid()[:8]}"

def generate_decision_id() -> str:
    return f"dec_{shortuuid.uuid()[:8]}"

def generate_user_id() -> str:
    return f"usr_{shortuuid.uuid()[:8]}"
