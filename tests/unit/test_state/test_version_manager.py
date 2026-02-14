import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from src.state.version_manager import VersionManager
from src.state.state_schema import TaskStateSchema
from datetime import datetime

@pytest.mark.asyncio
async def test_create_snapshot():
    # Use patch to avoid real MongoDB connection in __init__
    with patch("src.state.version_manager.AsyncIOMotorClient") as mock_client:
        mock_db = mock_client.return_value[ "test_db" ]
        mock_collection = mock_db.state_history
        mock_collection.insert_one = AsyncMock(return_value=MagicMock())

        manager = VersionManager()
        state = TaskStateSchema(task_id="t1", user_id="u1", goal={"r": "g"})

        success = await manager.create_snapshot(state)

        assert success is True
        mock_collection.insert_one.assert_called_once()
        # Verify snapshot contains task_id
        call_args = mock_collection.insert_one.call_args[0][0]
        assert call_args["task_id"] == "t1"
        assert "snapshot_at" in call_args

@pytest.mark.asyncio
async def test_get_history():
    with patch("src.state.version_manager.AsyncIOMotorClient") as mock_client:
        mock_db = mock_client.return_value[ "test_db" ]
        mock_collection = mock_db.state_history

        # Mock cursor for find()
        mock_cursor = MagicMock()
        mock_cursor.sort.return_value = mock_cursor

        # Mocking async iterator
        history_docs = [
            {"task_id": "t1", "user_id": "u1", "goal": {"r": "g"}, "status": "pending", "updated_at": datetime.utcnow(), "created_at": datetime.utcnow()},
            {"task_id": "t1", "user_id": "u1", "goal": {"r": "g"}, "status": "completed", "updated_at": datetime.utcnow(), "created_at": datetime.utcnow()}
        ]

        async def mock_async_iter():
            for doc in history_docs:
                yield doc

        mock_cursor.__aiter__.side_effect = mock_async_iter
        mock_collection.find.return_value = mock_cursor

        manager = VersionManager()
        history = await manager.get_history("t1")

        assert len(history) == 2
        assert history[0].task_id == "t1"
        mock_collection.find.assert_called_once_with({"task_id": "t1"})
