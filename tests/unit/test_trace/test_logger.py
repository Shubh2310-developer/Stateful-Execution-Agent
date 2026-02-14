import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from src.trace.trace_logger import TraceLogger
from datetime import datetime

@pytest.mark.asyncio
async def test_trace_log_event():
    with patch("src.trace.trace_logger.AsyncIOMotorClient") as mock_client:
        mock_db = mock_client.return_value["test_db"]
        mock_collection = mock_db.trace
        mock_collection.insert_one = AsyncMock(return_value=MagicMock())

        logger = TraceLogger()
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
