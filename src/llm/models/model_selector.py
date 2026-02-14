from typing import Optional
from src.llm.models.model_config import MODELS, DEFAULT_MODEL
from src.core.config import settings

class ModelSelector:
    @staticmethod
    def get_model(task_type: Optional[str] = None) -> str:
        # For now, return the default model or one from settings
        # Could be expanded to select cheaper models for simple tasks
        return settings.llm.model or DEFAULT_MODEL

    @staticmethod
    def get_model_info(model_name: str) -> dict:
        return MODELS.get(model_name, MODELS[DEFAULT_MODEL])
