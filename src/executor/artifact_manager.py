import os
from typing import Any, Dict, Optional
from uuid import uuid4
from src.core.types import Artifact
from src.utils.logger import logger
from src.state.persistence.database_adapter import DatabaseAdapter
from src.storage.artifact_store import ArtifactStore

class ArtifactManager:
    """Manages the creation, storage, and retrieval of execution artifacts."""

    def __init__(
        self,
        db_adapter: Optional[DatabaseAdapter] = None,
        store: Optional[ArtifactStore] = None
    ):
        self.db_adapter = db_adapter
        self.store = store or ArtifactStore()

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

        # Delegate storage and metadata calculation to ArtifactStore
        storage_info = await self.store.store_artifact(
            task_id=task_id,
            artifact_id=artifact_id,
            content=content,
            extension=format
        )

        # Generate preview for metadata if applicable
        preview = self.store.get_artifact_preview(
            content=content,
            mime_type=storage_info["mime_type"]
        )

        artifact_metadata = metadata or {}
        artifact_metadata["preview"] = preview

        artifact = Artifact(
            id=artifact_id,
            task_id=task_id,
            step_id=step_id,
            type=artifact_type,
            uri=storage_info["uri"],
            checksum=storage_info["checksum"],
            size_bytes=storage_info["size_bytes"],
            mime_type=storage_info["mime_type"],
            metadata=artifact_metadata,
            created_at=storage_info["created_at"]
        )

        logger.info(f"Artifact created: {artifact_id} via store")

        # Register in database if adapter is present
        if self.db_adapter:
            await self.db_adapter.register_artifact(artifact)

        return artifact

    def get_artifact_content(self, artifact: Artifact) -> Any:
        # Determine format/extension from URI
        uri = artifact.uri
        filename = os.path.basename(uri)
        ext = os.path.splitext(filename)[1].lower().replace(".", "") or "json"

        return self.store.retrieve_artifact(
            task_id=artifact.task_id,
            artifact_id=artifact.id,
            extension=ext
        )
