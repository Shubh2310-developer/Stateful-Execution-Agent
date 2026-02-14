import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from src.state.state_manager import StateManager
from src.state.state_schema import TaskStateSchema
from datetime import datetime

@pytest.mark.asyncio
async def test_initialize_state():
    with patch("src.state.state_manager.DatabaseAdapter") as mock_adapter_cls:
        mock_adapter = mock_adapter_cls.return_value
        mock_adapter.save_state = AsyncMock(return_value=True)

        manager = StateManager()
        task_id = "task_1"
        user_id = "user_1"
        goal = {"request": "test goal"}

        state = await manager.initialize_state(task_id, user_id, goal)

        assert state.task_id == task_id
        assert state.user_id == user_id
        assert state.status == "pending"
        assert state.goal == goal
        mock_adapter.save_state.assert_called_once()

@pytest.mark.asyncio
async def test_get_state():
    with patch("src.state.state_manager.DatabaseAdapter") as mock_adapter_cls:
        mock_adapter = mock_adapter_cls.return_value
        expected_state = TaskStateSchema(task_id="t1", user_id="u1", goal={"r": "g"})
        mock_adapter.load_state = AsyncMock(return_value=expected_state)

        manager = StateManager()
        state = await manager.get_state("t1")

        assert state.task_id == "t1"
        mock_adapter.load_state.assert_called_once_with("t1")

@pytest.mark.asyncio
async def test_update_status():
    with patch("src.state.state_manager.DatabaseAdapter") as mock_adapter_cls:
        mock_adapter = mock_adapter_cls.return_value
        initial_state = TaskStateSchema(task_id="t1", user_id="u1", goal={"r": "g"}, status="pending")
        mock_adapter.load_state = AsyncMock(return_value=initial_state)
        mock_adapter.save_state = AsyncMock(return_value=True)

        manager = StateManager()
        success = await manager.update_status("t1", "in_progress")

        assert success is True
        assert initial_state.status == "in_progress"
        mock_adapter.save_state.assert_called_once()
