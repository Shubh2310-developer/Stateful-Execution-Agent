from typing import Any, Dict, Optional
from src.storage.local_storage import LocalStorage
from src.utils.logger import logger

class ArtifactStore:
    """Abstraction layer for storing and retrieving execution artifacts."""

    def __init__(self, backend_type: str = "local"):
        self.backend = LocalStorage()
        if backend_type != "local":
            logger.warning(f"Storage backend {backend_type} not implemented, falling back to local.")

    def store_artifact(self, task_id: str, artifact_id: str, content: Any, extension: str = "json") -> str:
        key = f"{task_id}/{artifact_id}.{extension}"
        return self.backend.put(key, content)

    def retrieve_artifact(self, task_id: str, artifact_id: str, extension: str = "json") -> Any:
        key = f"{task_id}/{artifact_id}.{extension}"
        return self.backend.get(key)
