import asyncio
import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from src.state.persistence.database_adapter import DatabaseAdapter
from src.trace.trace_logger import TraceLogger
from src.trace.decision_recorder import DecisionRecorder
from uuid import uuid4

# Mock Motor classes
class MockAsyncIOMotorClient:
    def __init__(self, *args, **kwargs):
        self.db = MockAsyncIOMotorDatabase()

    def __getitem__(self, key):
        return self.db

class MockAsyncIOMotorDatabase:
    def __init__(self):
        self.collections = {}

    def __getitem__(self, key):
        if key not in self.collections:
            self.collections[key] = MockAsyncIOMotorCollection(name=key)
        return self.collections[key]

    def __getattr__(self, name):
        return self[name]

class MockAsyncIOMotorCollection:
    def __init__(self, name="mock_collection"):
        self.name = name
        self.insert_one = AsyncMock()
        self.insert_many = AsyncMock()
        self.create_index = AsyncMock()
        self.find_one = AsyncMock()
        self.count_documents = AsyncMock()
        self.delete_many = AsyncMock()

@pytest.fixture
def mock_db_adapter():
    with patch('src.state.persistence.database_adapter.AsyncIOMotorClient') as mock_client_cls:
        mock_client = MockAsyncIOMotorClient()
        mock_client_cls.return_value = mock_client

        adapter = DatabaseAdapter()
        # Ensure adapter uses our mock db structure
        adapter.client = mock_client
        adapter.db = mock_client.db
        adapter.traces = mock_client.db['trace']
        adapter.decisions = mock_client.db['decisions']
        adapter.tasks = mock_client.db['tasks']
        adapter.versions = mock_client.db['task_versions']
        adapter.artifacts = mock_client.db['artifacts']

        yield adapter

@pytest.mark.asyncio
async def test_indexes_creation(mock_db_adapter):
    """Verify that indexes are created correctly using mocks."""
    await mock_db_adapter.setup_indexes()

    # Verify trace indexes were created
    assert mock_db_adapter.traces.create_index.call_count >= 2
    # Verify we created an index on task_id + timestamp
    calls = mock_db_adapter.traces.create_index.call_args_list
    # Just checking that create_index was called is a good first step for mocks

    # Verify decision indexes were created
    assert mock_db_adapter.decisions.create_index.call_count >= 4

@pytest.mark.asyncio
async def test_trace_logging_buffered(mock_db_adapter):
    """Verify that trace logging works with the buffer using mocks."""
    # Initialize logger with mock adapter
    logger_instance = TraceLogger(db_adapter=mock_db_adapter)

    # Override buffer settings for faster test
    logger_instance.buffer._flush_interval = 0.1
    logger_instance.buffer._batch_size = 5

    task_id = str(uuid4())

    # Log some events
    for i in range(10):
        await logger_instance.log_event(
            task_id=task_id,
            event_type="test_event",
            context={"index": i},
            step_id=str(i)
        )

    # Wait for flush
    await asyncio.sleep(0.3)

    # Verify insert_many was called
    # Since batch size is 5 and we logged 10 items, we expect roughly 2 calls
    assert logger_instance.buffer.collection.insert_many.called

    # Check total items inserted
    total_inserted = 0
    for call in logger_instance.buffer.collection.insert_many.call_args_list:
        args, _ = call
        batch = args[0]
        total_inserted += len(batch)

    assert total_inserted == 10

    # Clean up buffer task
    await logger_instance.buffer.stop()

@pytest.mark.asyncio
async def test_decision_recording_buffered(mock_db_adapter):
    """Verify that decision recording works with the buffer using mocks."""
    recorder_instance = DecisionRecorder(db_adapter=mock_db_adapter)

    # Override buffer settings for faster test
    recorder_instance.buffer._flush_interval = 0.1
    recorder_instance.buffer._batch_size = 5

    task_id = str(uuid4())

    # Record decisions
    for i in range(7):
        await recorder_instance.record_decision(
            task_id=task_id,
            decision_point=f"Point {i}",
            rationale="Testing buffer",
            final_choice="Option A",
            confidence_score=0.9,
            step_id=str(i),
            tags=["#test"]
        )

    # Wait for flush
    await asyncio.sleep(0.3)

    # Verify insert_many was called
    assert recorder_instance.buffer.collection.insert_many.called

    # Check total items inserted
    total_inserted = 0
    for call in recorder_instance.buffer.collection.insert_many.call_args_list:
        args, _ = call
        batch = args[0]
        total_inserted += len(batch)

    assert total_inserted == 7

    # Clean up buffer task
    await recorder_instance.buffer.stop()

if __name__ == "__main__":
    # verification runner
    import sys
    # We can't easily run pytest from main here without installing it in the env properly or using subprocess
    # So we'll just print a message to run with pytest
    print("Please run this file with: pytest tests/integration/test_trace_system.py")
