import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, timezone

# We need to mock the database clients BEFORE importing app
# because they are initialized at module level in routes

@pytest.fixture
def mock_query_engine():
    with patch("src.api.routes.trace.query_engine") as mock_engine:
        mock_engine.query_traces = AsyncMock(return_value=[])
        mock_engine.get_decisions_by_task = AsyncMock(return_value=[])
        mock_engine.get_step_trace = AsyncMock(return_value=[])
        mock_engine.get_low_confidence_decisions = AsyncMock(return_value=[])
        mock_engine.search_reasoning = AsyncMock(return_value=[])
        yield mock_engine

@pytest.fixture
def mock_trace_logger():
    with patch("src.trace.trace_logger.trace_logger") as mock_logger:
        mock_logger.log_event = AsyncMock(return_value="trace_id_123")
        yield mock_logger

@pytest.fixture
def mock_decision_recorder():
    with patch("src.trace.decision_recorder.decision_recorder") as mock_recorder:
        mock_recorder.record_decision = AsyncMock(return_value="decision_id_123")
        yield mock_recorder

# Patch the mongo client to avoid connection errors during app import if possible
# or just ignore the background errors if we mock the logic that uses them.
# However, importing app will start the app...
from src.api.app import app

@pytest.mark.asyncio
async def test_trace_api_endpoints(mock_query_engine, mock_trace_logger, mock_decision_recorder):
    """Test the trace API endpoints with mocked query engine."""

    task_id = "task_123"
    step_id = "step_456"

    # Setup mock returns
    mock_trace_entry = {
        "trace_id": "trace_1",
        "task_id": task_id,
        "step_id": step_id,
        "event_type": "test_event",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "context": {"test": "data"},
        "metadata": {},
        "tags": []
    }
    mock_query_engine.query_traces.return_value = [mock_trace_entry]

    mock_decision = {
        "decision_id": "dec_1",
        "task_id": task_id,
        "step_id": step_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "decision_point": "test_decision",
        "decision_rationale": "testing api",
        "final_choice": "choice_a",
        "confidence_score": 0.4,
        "options_considered": [],
        "metadata": {},
        "tags": []
    }
    mock_query_engine.get_decisions_by_task.return_value = [mock_decision]
    mock_query_engine.get_step_trace.return_value = [mock_trace_entry]
    mock_query_engine.get_low_confidence_decisions.return_value = [mock_decision]
    mock_query_engine.search_reasoning.return_value = [mock_decision]

    # Add authentication headers
    auth_headers = {"Authorization": "Bearer demo-token-123"}

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # 2. Test get_task_traces
        response = await ac.get(f"/api/v1/trace/task/{task_id}", headers=auth_headers)
        assert response.status_code == 200
        traces = response.json()
        assert len(traces) == 1
        assert traces[0]["task_id"] == task_id

        # 3. Test get_task_decisions
        response = await ac.get(f"/api/v1/trace/task/{task_id}/decisions", headers=auth_headers)
        assert response.status_code == 200
        decisions = response.json()
        assert len(decisions) == 1
        assert decisions[0]["decision_point"] == "test_decision"

        # 4. Test get_step_traces
        response = await ac.get(f"/api/v1/trace/task/{task_id}/step/{step_id}", headers=auth_headers)
        assert response.status_code == 200

        # 5. Test get_low_confidence_decisions
        response = await ac.get("/api/v1/trace/search/low-confidence?threshold=0.5", headers=auth_headers)
        assert response.status_code == 200

        # 6. Test search_reasoning
        response = await ac.get("/api/v1/trace/search/reasoning?keyword=testing", headers=auth_headers)
        assert response.status_code == 200

@pytest.mark.asyncio
async def test_trace_context_middleware():
    """Test that middleware captures headers."""
    task_id = "task_ctx_123"

    # We use auth headers here too since root "/" is public but good to be consistent if we changed endpoint
    # Actually "/" is public, so no auth needed for it based on middleware code

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        headers = {"X-Task-ID": task_id, "X-Step-ID": "step_123"}
        response = await ac.get("/", headers=headers)
        assert response.status_code == 200
        assert "X-Request-ID" in response.headers

