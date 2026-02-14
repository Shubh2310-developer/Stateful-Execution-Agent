import os
import pytest
from src.executor.artifact_manager import ArtifactManager
from src.storage.artifact_store import ArtifactStore

@pytest.mark.asyncio
async def test_create_artifact_json(tmp_path):
    # Setup ArtifactStore with temporary directory
    store = ArtifactStore(base_dir=str(tmp_path))
    manager = ArtifactManager(store=store)
    task_id = "test_task"
    step_id = "step_1"
    content = {"key": "value"}

    artifact = await manager.create_artifact(
        task_id=task_id,
        step_id=step_id,
        artifact_type="data",
        content=content,
        format="json"
    )

    assert artifact.task_id == task_id
    assert artifact.type == "data"
    assert artifact.checksum is not None
    assert artifact.size_bytes > 0
    # Extract filename from URI
    file_path = artifact.uri.replace("file://", "")
    assert os.path.exists(file_path)

    # Verify content retrieval
    retrieved = manager.get_artifact_content(artifact)
    assert retrieved == content

@pytest.mark.asyncio
async def test_create_artifact_text(tmp_path):
    store = ArtifactStore(base_dir=str(tmp_path))
    manager = ArtifactManager(store=store)
    content = "Hello, world!"

    artifact = await manager.create_artifact(
        "task_1", "step_1", "document", content, format="txt"
    )

    assert artifact.type == "document"
    retrieved = manager.get_artifact_content(artifact)
    assert retrieved == content
