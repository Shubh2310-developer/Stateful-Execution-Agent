import os
import json
from typing import Any, Dict, Optional
from datetime import datetime
from uuid import uuid4
from src.core.types import Artifact
from src.core.config import settings
from src.utils.logger import logger

class ArtifactManager:
    """Manages the creation, storage, and retrieval of execution artifacts."""

    def __init__(self, base_path: str = "artifacts"):
        self.base_path = base_path
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)

    async def create_artifact(
        self,
        task_id: str,
        step_id: str,
        artifact_type: str,
        content: Any,
        format: str = "json",
        metadata: Optional[Dict[str, Any]] = None
    ) -> Artifact:
        artifact_id = f"art_{uuid4().hex[:8]}"
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"{task_id}_{step_id}_{artifact_id}.{format}"
        file_path = os.path.join(self.base_path, filename)

        # Handle different content types
        if format == "json":
            with open(file_path, "w") as f:
                json.dump(content, f, indent=2)
        elif format in ["md", "txt"]:
            with open(file_path, "w") as f:
                f.write(str(content))
        else:
            # For binary or other formats, assume content is already bytes/handled
            with open(file_path, "wb") as f:
                f.write(content)

        logger.info(f"Artifact created: {artifact_id} at {file_path}")

        return Artifact(
            artifact_id=artifact_id,
            task_id=task_id,
            step_id=step_id,
            type=artifact_type,
            format=format,
            storage_uri=f"file://{os.path.abspath(file_path)}",
            content_preview=str(content)[:200] if isinstance(content, (str, dict)) else None,
            metadata=metadata or {},
            created_at=datetime.utcnow()
        )

    def get_artifact_content(self, artifact: Artifact) -> Any:
        file_path = artifact.storage_uri.replace("file://", "")
        if not os.path.exists(file_path):
            logger.error(f"Artifact file not found: {file_path}")
            return None

        if artifact.format == "json":
            with open(file_path, "r") as f:
                return json.load(f)
        elif artifact.format in ["md", "txt"]:
            with open(file_path, "r") as f:
                return f.read()
        else:
            with open(file_path, "rb") as f:
                return f.read()
