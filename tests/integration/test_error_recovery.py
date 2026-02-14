import pytest
from unittest.mock import AsyncMock, patch
from src.orchestration.workflow_engine import WorkflowEngine
from src.core.types import TaskState

@pytest.mark.asyncio
async def test_error_recovery_flow():
    engine = WorkflowEngine()
    state = TaskState(
        task_id="t1", user_id="u1", status="paused",
        goal={"request": "retry me"}
    )

    # Mock executor to simulate recovery
    with patch.object(engine.executor, "execute_plan") as mock_execute:
        async def mock_recovery(s, user_memory=None):
            s.status = "completed"
            return s
        mock_execute.side_effect = mock_recovery

        updated_state = await engine.process_task(state, [])
        assert updated_state.status == "completed"
