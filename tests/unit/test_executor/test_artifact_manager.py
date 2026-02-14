import os
import json
import pytest
from src.executor.artifact_manager import ArtifactManager

def test_create_artifact_json(tmp_path):
    # Setup base path to temporary directory
    manager = ArtifactManager(base_path=str(tmp_path))
    task_id = "test_task"
    step_id = "step_1"
    content = {"key": "value"}

    # Use sync wrapper or just await it if running in loop
    import asyncio
    artifact = asyncio.run(manager.create_artifact(
        task_id=task_id,
        step_id=step_id,
        artifact_type="data",
        content=content,
        format="json"
    ))

    assert artifact.task_id == task_id
    assert artifact.format == "json"
    assert os.path.exists(artifact.storage_uri.replace("file://", ""))

    # Verify content retrieval
    retrieved = manager.get_artifact_content(artifact)
    assert retrieved == content

def test_create_artifact_text(tmp_path):
    manager = ArtifactManager(base_path=str(tmp_path))
    content = "Hello, world!"

    import asyncio
    artifact = asyncio.run(manager.create_artifact(
        "task_1", "step_1", "document", content, format="txt"
    ))

    assert artifact.format == "txt"
    retrieved = manager.get_artifact_content(artifact)
    assert retrieved == content
