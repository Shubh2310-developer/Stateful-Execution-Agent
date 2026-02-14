import pytest
from unittest.mock import AsyncMock, patch
from src.orchestration.workflow_engine import WorkflowEngine
from src.core.types import TaskState, Goal, TaskStatus, Plan

@pytest.mark.asyncio
async def test_error_recovery_flow():
    engine = WorkflowEngine()
    state = TaskState(
        task_id="t1", user_id="u1", status=TaskStatus.PAUSED,
        goal=Goal(request="retry me", success_criteria=["retried"])
    )

    # Mock planner and executor to simulate recovery
    with patch.object(engine.planner, "create_plan") as mock_create_plan, \
         patch.object(engine.executor, "execute_plan") as mock_execute:

        mock_create_plan.return_value = Plan(task_id="t1", steps=[])

        async def mock_recovery(s, user_memory=None):
            s.status = TaskStatus.COMPLETED
            return s
        mock_execute.side_effect = mock_recovery

        updated_state = await engine.process_task(state, [])
        assert updated_state.status == TaskStatus.COMPLETED
