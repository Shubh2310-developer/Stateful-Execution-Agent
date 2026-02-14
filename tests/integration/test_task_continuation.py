import pytest
from unittest.mock import AsyncMock, patch
from src.orchestration.task_router import TaskRouter

@pytest.mark.asyncio
async def test_task_continuation_flow():
    router = TaskRouter()
    task_id = "task_cont_1"
    user_id = "usr_test_123"

    # Mock session manager to return an existing session
    with patch.object(router.session_manager, "get_session") as mock_get_session, \
         patch.object(router.workflow_engine, "process_task") as mock_process, \
         patch.object(router.session_manager, "close_session") as mock_close:

        from src.state.state_schema import TaskStateSchema
        from datetime import datetime

        existing_state = TaskStateSchema(
            task_id=task_id,
            user_id=user_id,
            goal={"request": "Step 1"},
            status="paused"
        )
        mock_get_session.return_value = existing_state

        # Mock successful processing
        updated_state = existing_state.copy()
        updated_state.status = "completed"
        mock_process.return_value = updated_state

        result = await router.handle_request(
            user_id=user_id,
            goal="Add step 2",
            task_id=task_id
        )

        assert result["status"] == "completed"
        mock_get_session.assert_called_once_with(task_id)
        mock_process.assert_called_once()
        mock_close.assert_called_once_with(task_id)
