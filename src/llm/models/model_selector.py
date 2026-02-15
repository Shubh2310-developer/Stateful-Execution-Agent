from typing import Optional
from src.llm.models.model_config import MODELS, DEFAULT_MODEL
from src.core.config import settings

class ModelSelector:
    @staticmethod
    def get_model(task_type: Optional[str] = None) -> str:
        """
        Selects the appropriate model based on task complexity.

        Routing Strategy:
        - planning, review: Premium model (llama-3.3-70b-versatile)
        - extraction, quality_check, tool_params: Balanced model (mixtral-8x7b-32768)
        - summary, simple_task: Efficient model (llama3-8b-8192)
        """
        if not task_type:
            return settings.llm.model or DEFAULT_MODEL

        # Task-based routing
        if task_type in ["planning", "review", "complex_reasoning"]:
            return "llama-3.3-70b-versatile"
        elif task_type in ["extraction", "quality_check", "tool_params", "validation"]:
            return "mixtral-8x7b-32768"
        elif task_type in ["summary", "simple_task", "translation"]:
            return "llama3-8b-8192"

        return settings.llm.model or DEFAULT_MODEL

    @staticmethod
    def get_model_info(model_name: str) -> dict:
        return MODELS.get(model_name, MODELS[DEFAULT_MODEL])
