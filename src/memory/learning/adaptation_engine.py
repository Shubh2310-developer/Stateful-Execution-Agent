from typing import Dict, Any, List, Optional
from src.core.types import TaskState, UserMemory
from src.utils.logger import logger

class AdaptationEngine:
    """Extracts lessons from completed tasks to update long-term memory."""

    async def learn_from_task(self, state: TaskState, feedback: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        logger.info(f"Learning from task: {state.task_id}")

        # Extract successful patterns
        if state.status == "completed":
            pattern = {
                "task_type": state.goal.get("request", "unknown"),
                "approach": f"Successfully completed {len(state.plan.steps if state.plan else [])} steps.",
                "success_score": 1.0,
                "timestamp": state.updated_at
            }

            if feedback:
                pattern["feedback"] = feedback.get("content")
                pattern["rating"] = feedback.get("rating")

            return pattern

        return {}
