from typing import List, Dict, Any, Optional
from src.core.types import TaskState
from src.core.exceptions import ValidationError
from src.utils.logger import logger

class StateValidator:
    """Validates task state integrity and transitions."""

    def validate_transition(self, current_status: str, next_status: str):
        valid_transitions = {
            "pending": ["planning", "failed"],
            "planning": ["planned", "failed"],
            "planned": ["in_progress", "failed"],
            "in_progress": ["completed", "paused", "failed"],
            "paused": ["in_progress", "planning", "failed"],
            "completed": [],
            "failed": ["planning"]
        }

        if next_status not in valid_transitions.get(current_status, []):
            logger.warning(f"Invalid state transition: {current_status} -> {next_status}")
            return False
        return True

    def check_integrity(self, state: TaskState) -> bool:
        if not state.task_id or not state.user_id:
            raise ValidationError("Task ID and User ID are required.")

        if state.status == "completed" and state.current_step_index < len(state.plan.steps if state.plan else []):
            raise ValidationError("Task marked as completed but not all steps finished.")

        return True
