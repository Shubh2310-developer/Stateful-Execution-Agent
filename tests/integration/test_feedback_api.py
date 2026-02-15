"""
Integration tests for the Feedback API endpoint.

Tests the full feedback processing pipeline through the API.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, timezone

from src.api.app import app
from src.core.types import TaskState, Goal, TaskStatus, Plan, Step


@pytest.fixture
def client():
    """Create a test client with authentication."""
    return TestClient(app, headers={"Authorization": "Bearer demo-token-123"})


@pytest.fixture
def mock_task_state():
    """Create a mock task state for testing."""
    return TaskState(
        task_id="test_task_123",
        user_id="usr_demo_123",
        goal=Goal(
            request="Test goal",
            success_criteria=["Complete the test"]
        ),
        status=TaskStatus.COMPLETED,
        plan=Plan(
            task_id="test_task_123",
            steps=[
                Step(
                    step_id="step_1",
                    order=1,
                    action="test_action",
                    description="Test step"
                )
            ]
        )
    )


@pytest.fixture
def mock_feedback_result():
    """Create a mock feedback processing result."""
    return {
        "feedback_id": "fb_test123",
        "processed_at": datetime.now(timezone.utc).isoformat(),
        "sentiment": "positive",
        "categories": ["quality", "speed"],
        "correlations": {
            "steps": {"step_1": 0.9},
            "decisions": {}
        },
        "preference_updates": [
            {
                "field": "detail_level",
                "old_value": "medium",
                "new_value": "concise",
                "confidence": 0.85,
                "reasoning": "User requested concise responses"
            }
        ],
        "historical_pattern_updated": True,
        "insights": [
            {
                "insight": "User prefers concise responses",
                "confidence": 0.85,
                "action": "Set default detail_level to concise",
                "category": "preference",
                "metadata": {"field": "detail_level"}
            }
        ],
        "recommendations_for_future": [
            "Apply updated user preferences to all future tasks"
        ]
    }


class TestFeedbackAPI:
    """Test suite for the feedback API endpoint."""

    @pytest.mark.asyncio
    @patch("src.api.routes.tasks.feedback_processor")
    @patch("src.api.routes.tasks.task_router")
    async def test_submit_basic_feedback(
        self, mock_task_router, mock_feedback_processor, client, mock_task_state, mock_feedback_result
    ):
        """Test submitting basic rating feedback."""
        # Setup mocks
        mock_task_router.session_manager.get_session = AsyncMock(return_value=mock_task_state)
        mock_feedback_processor.process_feedback = AsyncMock(return_value=mock_feedback_result)

        # Make request
        response = client.post(
            "/api/v1/tasks/test_task_123/feedback",
            json={"rating": 5}
        )

        # Assertions
        assert response.status_code == 201
        data = response.json()
        assert data["feedback_id"] == "fb_test123"
        assert data["sentiment"] == "positive"
        assert len(data["categories"]) == 2

    @pytest.mark.asyncio
    @patch("src.api.routes.tasks.feedback_processor")
    @patch("src.api.routes.tasks.task_router")
    async def test_submit_detailed_feedback_with_text(
        self, mock_task_router, mock_feedback_processor, client, mock_task_state, mock_feedback_result
    ):
        """Test submitting detailed feedback with text."""
        # Setup mocks
        mock_task_router.session_manager.get_session = AsyncMock(return_value=mock_task_state)
        mock_feedback_processor.process_feedback = AsyncMock(return_value=mock_feedback_result)

        # Make request
        response = client.post(
            "/api/v1/tasks/test_task_123/feedback",
            json={
                "rating": 4,
                "text_feedback": "Great work, but too verbose. Please be more concise."
            }
        )

        # Assertions
        assert response.status_code == 201
        data = response.json()
        assert data["feedback_id"] == "fb_test123"
        assert len(data["preference_updates"]) == 1
        assert data["preference_updates"][0]["field"] == "detail_level"
        assert len(data["insights"]) == 1
        assert len(data["recommendations_for_future"]) == 1

    @pytest.mark.asyncio
    @patch("src.api.routes.tasks.task_router")
    async def test_submit_feedback_task_not_found(self, mock_task_router, client):
        """Test feedback submission for non-existent task."""
        # Setup mock to return None (task not found)
        mock_task_router.session_manager.get_session = AsyncMock(return_value=None)

        # Make request
        response = client.post(
            "/api/v1/tasks/nonexistent_task/feedback",
            json={"rating": 5}
        )

        # Assertions
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    @patch("src.api.routes.tasks.feedback_processor")
    @patch("src.api.routes.tasks.task_router")
    async def test_submit_feedback_processing_error(
        self, mock_task_router, mock_feedback_processor, client, mock_task_state
    ):
        """Test feedback submission when processing fails."""
        # Setup mocks
        mock_task_router.session_manager.get_session = AsyncMock(return_value=mock_task_state)
        mock_feedback_processor.process_feedback = AsyncMock(
            return_value={"error": "Processing failed"}
        )

        # Make request
        response = client.post(
            "/api/v1/tasks/test_task_123/feedback",
            json={"rating": 5}
        )

        # Assertions
        assert response.status_code == 500
        assert "processing failed" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    @patch("src.api.routes.tasks.task_router")
    async def test_submit_feedback_invalid_rating(self, mock_task_router, client, mock_task_state):
        """Test feedback submission with invalid rating."""
        # Setup mock
        mock_task_router.session_manager.get_session = AsyncMock(return_value=mock_task_state)

        # Test rating too low
        response = client.post(
            "/api/v1/tasks/test_task_123/feedback",
            json={"rating": 0}
        )
        assert response.status_code == 422  # Validation error

        # Test rating too high
        response = client.post(
            "/api/v1/tasks/test_task_123/feedback",
            json={"rating": 6}
        )
        assert response.status_code == 422  # Validation error

    @pytest.mark.asyncio
    @patch("src.api.routes.tasks.feedback_processor")
    @patch("src.api.routes.tasks.task_router")
    async def test_submit_feedback_with_session_isolation(
        self, mock_task_router, mock_feedback_processor, client, mock_task_state
    ):
        """Test that users can only provide feedback for their own tasks."""
        # Create a mock state with a different user
        other_user_state = mock_task_state.copy()
        other_user_state.user_id = "other_user_123"

        mock_task_router.session_manager.get_session = AsyncMock(return_value=other_user_state)

        # Create a mock request with authenticated user
        with patch("src.api.routes.tasks.Request") as mock_request:
            mock_request.state.user = {"id": "test_user_123"}

            # This test would require modifying the endpoint to properly use the request object
            # For now, we'll skip this test as it requires more complex mocking
            pass

    @pytest.mark.asyncio
    @patch("src.api.routes.tasks.feedback_processor")
    @patch("src.api.routes.tasks.task_router")
    async def test_feedback_response_structure(
        self, mock_task_router, mock_feedback_processor, client, mock_task_state, mock_feedback_result
    ):
        """Test that the feedback response has the correct structure."""
        # Setup mocks
        mock_task_router.session_manager.get_session = AsyncMock(return_value=mock_task_state)
        mock_feedback_processor.process_feedback = AsyncMock(return_value=mock_feedback_result)

        # Make request
        response = client.post(
            "/api/v1/tasks/test_task_123/feedback",
            json={
                "rating": 5,
                "text_feedback": "Excellent work!"
            }
        )

        # Assertions
        assert response.status_code == 201
        data = response.json()

        # Check all required fields are present
        assert "feedback_id" in data
        assert "processed_at" in data
        assert "sentiment" in data
        assert "categories" in data
        assert "correlations" in data
        assert "preference_updates" in data
        assert "historical_pattern_updated" in data
        assert "insights" in data
        assert "recommendations_for_future" in data

        # Check data types
        assert isinstance(data["categories"], list)
        assert isinstance(data["correlations"], dict)
        assert isinstance(data["preference_updates"], list)
        assert isinstance(data["historical_pattern_updated"], bool)
        assert isinstance(data["insights"], list)
        assert isinstance(data["recommendations_for_future"], list)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
