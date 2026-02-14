import pytest
from unittest.mock import AsyncMock, MagicMock
from src.state.version_manager import VersionManager
from src.state.state_schema import TaskStateSchema
from datetime import datetime

@pytest.fixture
def mock_db_adapter():
    adapter = MagicMock()
    adapter.versions = MagicMock()
    adapter.save_state = AsyncMock()
    adapter.get_state_history = AsyncMock()
    return adapter

@pytest.mark.asyncio
async def test_create_snapshot(mock_db_adapter):
    manager = VersionManager(db_adapter=mock_db_adapter)
    state = TaskStateSchema(
        task_id="t1",
        user_id="u1",
        goal={
            "request": "test goal",
            "success_criteria": ["done"]
        },
        version_counter=1
    )

    mock_db_adapter.save_state.return_value = True
    success = await manager.create_snapshot(state, summary="Checkpoint")

    assert success is True
    mock_db_adapter.save_state.assert_called_once_with(
        state, is_milestone=True, summary="Checkpoint"
    )

@pytest.mark.asyncio
async def test_get_history(mock_db_adapter):
    manager = VersionManager(db_adapter=mock_db_adapter)
    history_docs = [
        {"task_id": "t1", "version": 2, "snapshot": {}},
        {"task_id": "t1", "version": 1, "snapshot": {}}
    ]
    mock_db_adapter.get_state_history.return_value = history_docs

    history = await manager.get_history("t1")

    assert len(history) == 2
    assert history[0]["version"] == 2
    mock_db_adapter.get_state_history.assert_called_once_with("t1", limit=20)

@pytest.mark.asyncio
async def test_rollback(mock_db_adapter):
    manager = VersionManager(db_adapter=mock_db_adapter)

    snapshot_data = {
        "task_id": "t1",
        "user_id": "u1",
        "goal": {
            "request": "test goal",
            "success_criteria": ["done"]
        },
        "version_counter": 1,
        "status": "PENDING"
    }

    mock_db_adapter.versions.find_one = AsyncMock(return_value={
        "task_id": "t1",
        "version": 1,
        "snapshot": snapshot_data
    })
    mock_db_adapter.save_state.return_value = True

    rolled_back_state = await manager.rollback("t1", 1)

    assert rolled_back_state is not None
    assert rolled_back_state.task_id == "t1"
    mock_db_adapter.versions.find_one.assert_called_once_with({"task_id": "t1", "version": 1})
    mock_db_adapter.save_state.assert_called_once()
