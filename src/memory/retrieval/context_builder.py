from typing import Any, Dict, List, Optional
from src.core.types import UserMemory
from src.memory.short_term.task_context import TaskContext
from src.utils.logger import logger

class ContextBuilder:
    """Constructs the comprehensive prompt context from memory and state."""

    def build_context(
        self,
        task_context: TaskContext,
        user_memory: Optional[UserMemory] = None,
        relevant_history: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        logger.debug(f"Building context for task {task_context.task_id}")

        context = {
            "task_id": task_context.task_id,
            "active_step": task_context.active_step,
            "working_variables": task_context.working_variables,
            "recent_notes": task_context.temporary_notes[-5:] if task_context.temporary_notes else []
        }

        if user_memory:
            context["user_profile"] = user_memory.profile
            context["user_preferences"] = user_memory.preferences

        if relevant_history:
            context["relevant_past_experiences"] = relevant_history

        return context
