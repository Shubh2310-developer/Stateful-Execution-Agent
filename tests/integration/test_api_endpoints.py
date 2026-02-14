import pytest
from fastapi.testclient import TestClient
from src.api.app import app
from unittest.mock import AsyncMock, patch

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"

def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

@pytest.mark.asyncio
async def test_create_task_endpoint():
    task_data = {
        "user_id": "usr_test_123",
        "goal": "Test goal",
        "execution_mode": "autonomous"
    }

    # Mock the task_router.handle_request method
    with patch("src.api.routes.tasks.task_router.handle_request") as mock_handle:
        mock_handle.return_value = {
            "task_id": "task_mock_123",
            "status": "planned",
            "goal_summary": "Test goal"
        }

        response = client.post("/api/v1/tasks/create", json=task_data)

        assert response.status_code == 200
        assert response.json()["task_id"] == "task_mock_123"
        mock_handle.assert_called_once()

@pytest.mark.asyncio
async def test_get_task_status_endpoint():
    task_id = "task_mock_123"

    with patch("src.api.routes.tasks.task_router.session_manager.get_session") as mock_get_session:
        from src.state.state_schema import TaskStateSchema
        from datetime import datetime

        mock_state = TaskStateSchema(
            task_id=task_id,
            user_id="usr_test_123",
            goal={"request": "Test goal"},
            status="in_progress",
            updated_at=datetime.utcnow()
        )
        mock_get_session.return_value = mock_state

        response = client.get(f"/api/v1/tasks/{task_id}/status")

        assert response.status_code == 200
        assert response.json()["task_id"] == task_id
        assert response.json()["status"] == "in_progress"
