import pytest
from src.orchestration.task_router import TaskRouter
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_simulated_load():
    """Simulates multiple concurrent task requests."""
    router = TaskRouter()

    with patch.object(router.workflow_engine, "process_task") as mock_process:
        mock_process.return_value = AsyncMock()

        # Simulate 5 concurrent requests
        import asyncio
        tasks = [
            router.handle_request(user_id=f"user_{i}", goal=f"goal {i}")
            for i in range(5)
        ]

        results = await asyncio.gather(*tasks)
        assert len(results) == 5
