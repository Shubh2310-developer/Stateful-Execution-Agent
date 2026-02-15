from typing import Any, Dict, Optional
from src.storage.local_storage import LocalStorage
from src.utils.logger import logger

import hashlib
import json
import mimetypes
import os
from datetime import datetime, timezone
from typing import Any, Dict, Optional, Union

from src.storage.local_storage import LocalStorage
from src.utils.logger import logger


class ArtifactStore:
    """Abstraction layer for storing and retrieving execution artifacts with metadata and previews."""

    def __init__(self, backend_type: str = "local", base_dir: str = "data/artifacts"):
        if backend_type == "local":
            self.backend = LocalStorage(base_dir=base_dir)
        else:
            # Future: S3Storage()
            logger.warning(
                f"Storage backend {backend_type} not implemented, falling back to local."
            )
            self.backend = LocalStorage(base_dir=base_dir)

    def _calculate_metadata(self, content: bytes, filename: str) -> Dict[str, Any]:
        """Calculates size, checksum, and mime type."""
        sha256_hash = hashlib.sha256(content).hexdigest()
        size_bytes = len(content)
        mime_type, _ = mimetypes.guess_type(filename)

        return {
            "checksum": sha256_hash,
            "size_bytes": size_bytes,
            "mime_type": mime_type or "application/octet-stream",
        }

    async def store_artifact(
        self,
        task_id: str,
        artifact_id: str,
        content: Any,
        extension: str = "json",
    ) -> Dict[str, Any]:
        """
        Stores artifact content and returns metadata for the Artifact model.
        """
        key = f"{task_id}/{artifact_id}.{extension}"

        # Serialization logic
        if extension == "json":
            if not isinstance(content, (str, bytes, bytearray)):
                data = json.dumps(content, indent=2).encode("utf-8")
            else:
                data = content if isinstance(content, bytes) else content.encode("utf-8")
        elif isinstance(content, str):
            data = content.encode("utf-8")
        elif isinstance(content, (bytes, bytearray)):
            data = content
        else:
            data = str(content).encode("utf-8")

        uri = self.backend.put(key, data)
        metadata = self._calculate_metadata(data, key)

        return {
            "uri": uri,
            **metadata,
            "created_at": datetime.now(timezone.utc),
        }

    def retrieve_artifact(
        self, task_id: str, artifact_id: str, extension: str = "json"
    ) -> Optional[Union[Dict, str, bytes]]:
        """Retrieves and deserializes artifact content."""
        key = f"{task_id}/{artifact_id}.{extension}"
        data = self.backend.get(key)

        if data is None:
            return None

        if extension == "json":
            try:
                return json.loads(data.decode("utf-8"))
            except Exception as e:
                logger.error(f"Error decoding JSON artifact {key}: {e}")
                return data
        elif extension in ["md", "txt", "py", "js", "html", "css"]:
            try:
                return data.decode("utf-8")
            except Exception:
                return data

        return data

    def get_artifact_preview(
        self, content: Any, mime_type: str, max_chars: int = 500
    ) -> str:
        """
        Generates a text preview of the artifact content for LLM context.
        """
        if content is None:
            return ""

        if "json" in mime_type:
            if not isinstance(content, str):
                text = json.dumps(content, indent=2)
            else:
                text = content
        elif any(
            t in mime_type
            for t in ["text", "markdown", "javascript", "python", "html", "xml"]
        ):
            text = str(content)
        elif "image" in mime_type:
            return f"[Image Artifact: {mime_type}]"
        else:
            # For other binary types, just show metadata info
            size = len(content) if isinstance(content, (bytes, str, list, dict)) else "?"
            return f"[Binary Artifact: {mime_type}, size: {size} bytes]"

        if len(text) > max_chars:
            return text[:max_chars] + "\n... (truncated)"
        return text

    def delete_artifact(self, task_id: str, artifact_id: str, extension: str) -> bool:
        """Deletes an artifact from storage."""
        key = f"{task_id}/{artifact_id}.{extension}"
        return self.backend.delete(key)
