from typing import Any, Dict, Optional, Union
import json
from datetime import datetime
from uuid import UUID
from enum import Enum
from pydantic import BaseModel
from src.utils.logger import logger

class AgentJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder for complex agent types."""
    def default(self, obj: Any) -> Any:
        if isinstance(obj, BaseModel):
            return obj.dict()
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, UUID):
            return str(obj)
        if isinstance(obj, Enum):
            return obj.value
        if isinstance(obj, set):
            return list(obj)
        return super().default(obj)

class JSONSerializer:
    """Custom JSON serialization logic for complex agent objects."""

    @staticmethod
    def serialize(data: Any, indent: Optional[int] = None) -> str:
        """Serializes data to JSON string, handling Pydantic and complex types."""
        try:
            return json.dumps(data, cls=AgentJSONEncoder, indent=indent)
        except Exception as e:
            logger.error(f"Serialization failed: {str(e)}")
            raise

    @staticmethod
    def deserialize(json_str: str) -> Any:
        """Deserializes JSON string back to Python objects."""
        try:
            return json.loads(json_str)
        except Exception as e:
            logger.error(f"Deserialization failed: {str(e)}")
            raise
