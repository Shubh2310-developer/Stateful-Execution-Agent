import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from src.state.persistence.database_adapter import DatabaseAdapter
from src.state.state_schema import TaskStateSchema
from src.core.types import Artifact

@pytest.fixture
def mock_settings():
    with patch("src.state.persistence.database_adapter.settings") as mock:
        mock.database.mongodb_uri = "mongodb://localhost:27017"
        mock.database.mongodb_db = "test_db"
        yield mock

@pytest.mark.asyncio
async def test_database_adapter_initialization(mock_settings):
    with patch("src.state.persistence.database_adapter.AsyncIOMotorClient") as mock_client:
        adapter = DatabaseAdapter()
        assert adapter.tasks is not None
        assert adapter.versions is not None
        assert adapter.artifacts is not None

@pytest.mark.asyncio
async def test_database_adapter_save_load(mock_settings):
    with patch("src.state.persistence.database_adapter.AsyncIOMotorClient") as mock_client:
        mock_db = mock_client.return_value["test_db"]
        adapter = DatabaseAdapter()

        # Mock collections
        adapter.tasks = AsyncMock()
        adapter.versions = AsyncMock()

        state_data = {
            "task_id": "t1",
            "user_id": "u1",
            "goal": {
                "request": "test goal",
                "success_criteria": ["done"]
            },
            "status": "PENDING",
            "version_counter": 1
        }
        state = TaskStateSchema(**state_data)

        # Mock find_one_and_update to return the updated document
        adapter.tasks.find_one_and_update = AsyncMock(return_value={
            **state_data,
            "version_counter": 2
        })

        # Mock the transaction context manager
        mock_session = AsyncMock()
        mock_client.return_value.start_session = AsyncMock(return_value=mock_session)
        mock_session.__aenter__.return_value = mock_session

        # start_transaction in Motor is a regular method that returns an async context manager
        mock_transaction = AsyncMock()
        mock_session.start_transaction = MagicMock(return_value=mock_transaction)
        mock_transaction.__aenter__.return_value = mock_transaction
        mock_transaction.__aexit__.return_value = False

        # Test save as milestone
        success = await adapter.save_state(state, is_milestone=True, summary="Milestone 1")

        assert success is True
        adapter.tasks.find_one_and_update.assert_called_once()
        adapter.versions.insert_one.assert_called_once()

        # Test load
        adapter.tasks.find_one = AsyncMock(return_value=state_data)
        loaded_state = await adapter.load_state("t1")
        assert loaded_state.task_id == "t1"
        adapter.tasks.find_one.assert_called_once_with({"task_id": "t1"})

@pytest.mark.asyncio
async def test_database_adapter_artifact_registration(mock_settings):
    with patch("src.state.persistence.database_adapter.AsyncIOMotorClient") as mock_client:
        adapter = DatabaseAdapter()
        adapter.artifacts = AsyncMock()

        artifact = Artifact(
            id="art1",
            task_id="t1",
            uri="file:///tmp/test.txt",
            type="text",
            checksum="abc",
            size_bytes=10
        )

        success = await adapter.register_artifact(artifact)
        assert success is True
        adapter.artifacts.update_one.assert_called_once()
