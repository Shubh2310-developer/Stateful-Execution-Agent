import pytest
from unittest.mock import AsyncMock, patch
from src.state.state_manager import StateManager
from src.state.state_schema import TaskStateSchema
from src.core.types import Goal, TaskStatus
from datetime import datetime

@pytest.mark.asyncio
async def test_initialize_state():
    with patch("src.state.state_manager.DatabaseAdapter") as mock_adapter_cls:
        mock_adapter = mock_adapter_cls.return_value
        mock_adapter.save_state = AsyncMock(return_value=True)

        manager = StateManager()
        task_id = "task_1"
        user_id = "user_1"
        goal_data = {
            "request": "test goal",
            "success_criteria": ["criteria 1"]
        }

        state = await manager.initialize_state(task_id, user_id, goal_data)

        assert state.task_id == task_id
        assert state.user_id == user_id
        assert state.status == TaskStatus.PENDING
        assert isinstance(state.goal, Goal)
        assert state.checksum is not None
        assert state.version_counter == 1
        mock_adapter.save_state.assert_called_once()

@pytest.mark.asyncio
async def test_get_state_with_checksum_verification():
    with patch("src.state.state_manager.DatabaseAdapter") as mock_adapter_cls:
        mock_adapter = mock_adapter_cls.return_value

        goal = Goal(request="g", success_criteria=["c"])
        initial_state = TaskStateSchema(task_id="t1", user_id="u1", goal=goal)
        # Manually set a valid checksum
        manager = StateManager()
        initial_state.checksum = manager._calculate_checksum(initial_state)

        mock_adapter.load_state = AsyncMock(return_value=initial_state)

        state = await manager.get_state("t1")

        assert state.task_id == "t1"
        assert state.checksum == initial_state.checksum
        mock_adapter.load_state.assert_called_once_with("t1")

@pytest.mark.asyncio
async def test_update_status():
    with patch("src.state.state_manager.DatabaseAdapter") as mock_adapter_cls:
        mock_adapter = mock_adapter_cls.return_value
        goal = Goal(request="g", success_criteria=["c"])
        initial_state = TaskStateSchema(task_id="t1", user_id="u1", goal=goal, status=TaskStatus.PENDING)
        mock_adapter.load_state = AsyncMock(return_value=initial_state)
        mock_adapter.save_state = AsyncMock(return_value=True)

        manager = StateManager()
        success = await manager.update_status("t1", TaskStatus.EXECUTING)

        assert success is True
        assert initial_state.status == TaskStatus.EXECUTING
        mock_adapter.save_state.assert_called_once()
