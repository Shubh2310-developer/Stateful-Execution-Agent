import pytest
from unittest.mock import AsyncMock, patch
from src.orchestration.workflow_engine import WorkflowEngine
from src.core.types import TaskState, Plan
from tests.fixtures.sample_tasks import SAMPLE_TASK_DATA

@pytest.mark.asyncio
async def test_end_to_end_workflow_simulated():
    # This test simulates the workflow engine processing a task
    engine = WorkflowEngine()

    state = TaskState(
        task_id="task_e2e_1",
        user_id="usr_test_123",
        status="pending",
        goal={"request": "Write a report"}
    )

    available_tools = ["web_search", "document_generator"]

    # Mock Planner and Executor to avoid real API calls
    with patch.object(engine.planner, "create_plan") as mock_create_plan, \
         patch.object(engine.executor, "execute_plan") as mock_execute_plan:

        mock_plan = Plan(
            task_id="task_e2e_1",
            goal_summary="Write a report",
            steps=[]
        )
        mock_create_plan.return_value = mock_plan

        # Simulate execution completing the task
        async def mock_execute(s, user_memory=None):
            s.status = "completed"
            return s
        mock_execute_plan.side_effect = mock_execute

        updated_state = await engine.process_task(state, available_tools)

        assert updated_state.status == "completed"
        mock_create_plan.assert_called_once()
        mock_execute_plan.assert_called_once()
