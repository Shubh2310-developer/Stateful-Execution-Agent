import os
import pytest
import asyncio
from src.executor.artifact_manager import ArtifactManager
from src.storage.artifact_store import ArtifactStore

@pytest.mark.asyncio
async def test_artifact_manager_with_store(tmp_path):
    # Setup ArtifactStore with temporary directory
    store = ArtifactStore(base_dir=str(tmp_path))
    manager = ArtifactManager(store=store)

    task_id = "test_task"
    step_id = "step_1"

    # 1. Test JSON artifact
    json_content = {"result": "success", "data": [1, 2, 3]}
    json_artifact = await manager.create_artifact(
        task_id=task_id,
        step_id=step_id,
        artifact_type="data",
        content=json_content,
        format="json"
    )

    assert json_artifact.task_id == task_id
    assert json_artifact.mime_type == "application/json"
    assert "preview" in json_artifact.metadata
    assert "success" in json_artifact.metadata["preview"]

    retrieved_json = manager.get_artifact_content(json_artifact)
    assert retrieved_json == json_content

    # 2. Test Text artifact
    text_content = "This is a test artifact content."
    text_artifact = await manager.create_artifact(
        task_id=task_id,
        step_id=step_id,
        artifact_type="document",
        content=text_content,
        format="txt"
    )

    assert text_artifact.mime_type == "text/plain"
    assert text_artifact.metadata["preview"] == text_content

    retrieved_text = manager.get_artifact_content(text_artifact)
    assert retrieved_text == text_content

    # 3. Test Binary artifact
    binary_content = b"\x00\x01\x02\x03\xff"
    binary_artifact = await manager.create_artifact(
        task_id=task_id,
        step_id=step_id,
        artifact_type="binary",
        content=binary_content,
        format="bin"
    )

    assert binary_artifact.mime_type == "application/octet-stream"
    assert "Binary Artifact" in binary_artifact.metadata["preview"]

    retrieved_binary = manager.get_artifact_content(binary_artifact)
    assert retrieved_binary == binary_content

@pytest.mark.asyncio
async def test_artifact_store_direct(tmp_path):
    store = ArtifactStore(base_dir=str(tmp_path))

    # Test preview truncation
    long_content = "A" * 1000
    preview = store.get_artifact_preview(long_content, "text/plain", max_chars=10)
    assert len(preview) <= 30 # 10 chars + newline + "... (truncated)"
    assert "truncated" in preview

    # Test deletion
    task_id = "del_task"
    art_id = "art_123"
    await store.store_artifact(task_id, art_id, "content", "txt")
    assert store.backend.exists(f"{task_id}/{art_id}.txt")

    store.delete_artifact(task_id, art_id, "txt")
    assert not store.backend.exists(f"{task_id}/{art_id}.txt")
