from typing import Any, Dict, Optional
import json
from src.utils.logger import logger

class JSONSerializer:
    """Custom JSON serialization logic for complex agent objects."""

    @staticmethod
    def serialize(data: Any) -> str:
        return json.dumps(data, default=str)

    @staticmethod
    def deserialize(json_str: str) -> Any:
        return json.loads(json_str)
