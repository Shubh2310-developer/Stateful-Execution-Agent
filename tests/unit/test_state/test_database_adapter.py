import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from src.state.persistence.database_adapter import DatabaseAdapter
from src.state.state_schema import TaskStateSchema

@pytest.mark.asyncio
async def test_database_adapter_save_load():
    with patch("src.state.persistence.database_adapter.AsyncIOMotorClient") as mock_client:
        mock_db = mock_client.return_value["test_db"]
        mock_collection = mock_db.state
        mock_collection.update_one = AsyncMock(return_value=MagicMock())

        state_data = {"task_id": "t1", "user_id": "u1", "goal": {"r": "g"}, "status": "pending"}
        mock_collection.find_one = AsyncMock(return_value=state_data)

        adapter = DatabaseAdapter()
        state = TaskStateSchema(**state_data)

        # Test save
        success = await adapter.save_state(state)
        assert success is True
        mock_collection.update_one.assert_called_once()

        # Test load
        loaded_state = await adapter.load_state("t1")
        assert loaded_state.task_id == "t1"
        assert loaded_state.user_id == "u1"
        mock_collection.find_one.assert_called_once_with({"task_id": "t1"})

@pytest.mark.asyncio
async def test_database_adapter_delete():
    with patch("src.state.persistence.database_adapter.AsyncIOMotorClient") as mock_client:
        mock_db = mock_client.return_value["test_db"]
        mock_collection = mock_db.state
        mock_collection.delete_one = AsyncMock(return_value=MagicMock())

        adapter = DatabaseAdapter()
        success = await adapter.delete_state("t1")

        assert success is True
        mock_collection.delete_one.assert_called_once_with({"task_id": "t1"})
