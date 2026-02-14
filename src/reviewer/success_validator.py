from typing import Any, Dict, List
from src.core.types import TaskState
from src.utils.logger import logger

class SuccessValidator:
    """Validates if the overall task goal has been successfully achieved."""

    def validate_achievement(self, state: TaskState) -> Dict[str, Any]:
        logger.info(f"Validating goal achievement for task: {state.task_id}")

        # Check if all steps are completed
        total_steps = len(state.plan.steps) if state.plan else 0
        completed_steps = state.current_step_index

        if total_steps == 0:
            return {"achieved": False, "reason": "No plan exists"}

        achievement_ratio = completed_steps / total_steps

        # Check for presence of final artifacts
        # (This would be more sophisticated in a real system)
        has_artifacts = len(state.artifacts) > 0

        achieved = achievement_ratio >= 1.0 and has_artifacts

        return {
            "achieved": achieved,
            "achievement_ratio": achievement_ratio,
            "artifacts_count": len(state.artifacts),
            "reason": "All steps completed" if achieved else "Incomplete steps or missing artifacts"
        }
