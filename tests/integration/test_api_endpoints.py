import pytest
from fastapi.testclient import TestClient
from src.api.app import app
from unittest.mock import AsyncMock, patch
from src.core.config import settings

client = TestClient(app)
AUTH_HEADERS = {"Authorization": "Bearer demo-token-123"}

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"

def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_unauthorized_access():
    response = client.get("/api/v1/tasks/task_123")
    assert response.status_code == 401
    assert "Missing authentication credentials" in response.json()["detail"]

@pytest.mark.asyncio
async def test_create_task_endpoint():
    task_data = {
        "user_id": "usr_demo_123",
        "goal": "Test goal",
        "execution_mode": "autonomous"
    }

    # Mock the task_router.initialize_task method
    with patch("src.api.routes.tasks.task_router.initialize_task") as mock_init:
        from src.state.state_schema import TaskStateSchema
        from src.core.types import Goal, TaskStatus
        from datetime import datetime, timezone

        mock_state = TaskStateSchema(
            task_id="task_mock_123",
            user_id="usr_demo_123",
            goal=Goal(request="Test goal", success_criteria=[]),
            status=TaskStatus.PENDING,
            updated_at=datetime.now(timezone.utc)
        )
        mock_init.return_value = mock_state

        with patch("src.api.routes.tasks.task_router.run_task_cycle") as mock_run:
            response = client.post("/api/v1/tasks", json=task_data, headers=AUTH_HEADERS)

            assert response.status_code == 201
            assert response.json()["task_id"] == "task_mock_123"
            assert response.json()["status"] == "PENDING"
            mock_init.assert_called_once()
            # Background task should be called
            # Note: FastAPI BackgroundTasks are executed after the response is sent,
            # but since we are mocking the router method it's tracked if called.

@pytest.mark.asyncio
async def test_get_task_status_endpoint():
    task_id = "task_mock_123"

    with patch("src.api.routes.tasks.task_router.session_manager.get_session") as mock_get_session:
        from src.state.state_schema import TaskStateSchema
        from src.core.types import Goal, TaskStatus
        from datetime import datetime, timezone

        mock_state = TaskStateSchema(
            task_id=task_id,
            user_id="usr_demo_123",
            goal=Goal(request="Test goal", success_criteria=["Goal met"]),
            status=TaskStatus.EXECUTING,
            updated_at=datetime.now(timezone.utc)
        )
        mock_get_session.return_value = mock_state

        response = client.get(f"/api/v1/tasks/{task_id}", headers=AUTH_HEADERS)

        assert response.status_code == 200
        assert response.json()["task_id"] == task_id
        assert response.json()["status"] == TaskStatus.EXECUTING.value
        assert "progress" in response.json()

@pytest.mark.asyncio
async def test_continue_task_endpoint():
    task_id = "task_mock_123"
    update_data = {
        "user_input": "Please continue",
        "mode": "resume"
    }

    with patch("src.api.routes.tasks.task_router.session_manager.get_session") as mock_get_session, \
         patch("src.api.routes.tasks.task_router.handle_continuation") as mock_continue, \
         patch("src.api.routes.tasks.task_router.run_task_cycle") as mock_run:

        from src.state.state_schema import TaskStateSchema
        from src.core.types import Goal, TaskStatus
        from datetime import datetime, timezone

        mock_state = TaskStateSchema(
            task_id=task_id,
            user_id="usr_demo_123",
            goal=Goal(request="Test goal", success_criteria=[]),
            status=TaskStatus.PAUSED,
            updated_at=datetime.now(timezone.utc)
        )
        mock_get_session.return_value = mock_state

        mock_updated_state = mock_state.copy()
        mock_updated_state.status = TaskStatus.EXECUTING
        mock_continue.return_value = mock_updated_state

        response = client.post(f"/api/v1/tasks/{task_id}/continue", json=update_data, headers=AUTH_HEADERS)

        assert response.status_code == 200
        assert response.json()["status"] == "EXECUTING"
        mock_continue.assert_called_once()

@pytest.mark.asyncio
async def test_pause_task_endpoint():
    task_id = "task_mock_123"

    with patch("src.api.routes.tasks.task_router.session_manager.get_session") as mock_get_session, \
         patch("src.api.routes.tasks.task_router.session_manager.state_manager.save_state") as mock_save:

        from src.state.state_schema import TaskStateSchema
        from src.core.types import Goal, TaskStatus
        from datetime import datetime, timezone

        mock_state = TaskStateSchema(
            task_id=task_id,
            user_id="usr_demo_123",
            goal=Goal(request="Test goal", success_criteria=[]),
            status=TaskStatus.EXECUTING,
            updated_at=datetime.now(timezone.utc)
        )
        mock_get_session.return_value = mock_state

        response = client.post(f"/api/v1/tasks/{task_id}/pause", headers=AUTH_HEADERS)

        assert response.status_code == 200
        assert response.json()["status"] == "PAUSED"
        mock_save.assert_called_once()

@pytest.mark.asyncio
async def test_session_isolation_violation():
    task_id = "task_other_user"

    with patch("src.api.routes.tasks.task_router.session_manager.get_session") as mock_get_session:
        from src.state.state_schema import TaskStateSchema
        from src.core.types import Goal, TaskStatus
        from datetime import datetime, timezone

        # State belongs to a different user
        mock_state = TaskStateSchema(
            task_id=task_id,
            user_id="usr_other_456",
            goal=Goal(request="Other goal", success_criteria=["Other goal met"]),
            status=TaskStatus.EXECUTING,
            updated_at=datetime.now(timezone.utc)
        )
        mock_get_session.return_value = mock_state

        # Attempt to access with demo-token-123 (mapped to usr_demo_123)
        # Note: The route is /tasks/{task_id} (get_task_status) based on previous Read,
        # but in previous tests it was /tasks/{task_id}/status.
        # Let's check the code in src/api/routes/tasks.py again to be sure.
        # The Read of src/api/routes/tasks.py showed: @router.get("/{task_id}", response_model=TaskStatusResponse)
        # So the path is /api/v1/tasks/{task_id}
        response = client.get(f"/api/v1/tasks/{task_id}", headers=AUTH_HEADERS)

        assert response.status_code == 403
        assert "Not authorized" in response.json()["detail"]

def test_api_key_authentication():
    # Use the API key configured in settings
    headers = {"X-API-KEY": "dev-api-key-12345"}
    response = client.get("/api/v1/health", headers=headers)
    assert response.status_code == 200

    # Test protected endpoint with API key
    task_id = "task_api_key_test"
    with patch("src.api.routes.tasks.task_router.session_manager.get_session") as mock_get_session:
        from src.state.state_schema import TaskStateSchema
        from src.core.types import Goal, TaskStatus
        from datetime import datetime, timezone

        mock_state = TaskStateSchema(
            task_id=task_id,
            user_id="usr_api_key_user", # Matching user for API Key
            goal=Goal(request="Test goal", success_criteria=["Goal met"]),
            status=TaskStatus.EXECUTING,
            updated_at=datetime.now(timezone.utc)
        )
        mock_get_session.return_value = mock_state

        # Path is /api/v1/tasks/{task_id}
        response = client.get(f"/api/v1/tasks/{task_id}", headers=headers)
        assert response.status_code == 200
        assert response.json()["task_id"] == task_id

def test_rate_limiting():
    # We need to mock the rate limiter or simply trigger it
    # Since RateLimiter is global, let's patch the is_rate_limited method to simulate hitting the limit

    with patch("src.api.middleware.rate_limiting.rate_limiter.is_rate_limited") as mock_is_limited:
        # First calls are not limited
        mock_is_limited.return_value = False
        response = client.get("/api/v1/health", headers=AUTH_HEADERS)
        assert response.status_code == 200

        # Now simulate limit exceeded
        mock_is_limited.return_value = True
        response = client.get("/api/v1/health", headers=AUTH_HEADERS)
        assert response.status_code == 429
        assert "Rate limit exceeded" in response.json()["detail"]
