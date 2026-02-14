from typing import Any, Dict, Optional
import time
from src.utils.logger import logger

class CacheManager:
    """Manages short-term ephemeral data and LLM response caching."""

    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}

    def set(self, key: str, value: Any, ttl: int = 3600):
        self._cache[key] = {
            "value": value,
            "expiry": time.time() + ttl
        }

    def get(self, key: str) -> Optional[Any]:
        if key not in self._cache:
            return None

        item = self._cache[key]
        if time.time() > item["expiry"]:
            del self._cache[key]
            return None

        return item["value"]

    def clear(self):
        self._cache.clear()
