import pytest
from src.memory.learning.adaptation_engine import AdaptationEngine
from src.core.types import TaskState
from datetime import datetime

@pytest.mark.asyncio
async def test_memory_learning_from_completion():
    engine = AdaptationEngine()
    state = TaskState(
        task_id="t1", user_id="u1", status="completed",
        goal={"request": "test learning"},
        updated_at=datetime.utcnow()
    )

    feedback = {"content": "Good job", "rating": 5}
    pattern = await engine.learn_from_task(state, feedback)

    assert pattern["success_score"] == 1.0
    assert pattern["feedback"] == "Good job"
    assert pattern["rating"] == 5
    assert "test learning" in pattern["task_type"]
