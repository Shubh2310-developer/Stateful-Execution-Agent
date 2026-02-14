import pytest
from unittest.mock import AsyncMock, MagicMock
from src.trace.trace_logger import TraceLogger

@pytest.mark.asyncio
async def test_trace_log_event():
    # Setup mock database adapter
    mock_db = MagicMock()
    mock_collection = AsyncMock()
    mock_db.trace = mock_collection
    mock_db_adapter = MagicMock()
    mock_db_adapter.db = mock_db

    # Initialize logger with mock adapter (Dependency Injection)
    logger = TraceLogger(db_adapter=mock_db_adapter)

    trace_id = await logger.log_event(
        task_id="t1",
        event_type="execution",
        context={"step": 1},
        metadata={"duration_ms": 100}
    )

    assert trace_id.startswith("trace_")
    mock_collection.insert_one.assert_called_once()
    call_args = mock_collection.insert_one.call_args[0][0]
    assert call_args["task_id"] == "t1"
    assert call_args["event_type"] == "execution"
