import pytest
import json
from unittest.mock import AsyncMock, patch
from src.memory.learning.adaptation_engine import AdaptationEngine
from src.core.types import TaskState, Goal, TaskStatus
from datetime import datetime, timezone

@pytest.mark.asyncio
async def test_memory_learning_from_completion():
    # Mock Response from LLM
    mock_reflection = {
        "reasoning": "The task was completed successfully using a direct approach.",
        "insights": ["Direct implementation works for simple requests"],
        "corrections": [],
        "patterns": {
            "task_category": "test_learning",
            "successful_approach": "Used direct implementation",
            "confidence_score": 1.0
        },
        "user_preference_updates": {
            "preferred_language": "Python"
        }
    }

    # Mock Groq Client and Memory Manager
    with patch("src.memory.learning.adaptation_engine.groq_client") as mock_groq, \
         patch("src.memory.learning.adaptation_engine.MemoryManager") as mock_mm_class:

        mock_mm = mock_mm_class.return_value
        mock_mm.update_user_preferences = AsyncMock()
        mock_mm.add_historical_pattern = AsyncMock()

        mock_groq.generate_response = AsyncMock(return_value=json.dumps(mock_reflection))

        engine = AdaptationEngine(memory_manager=mock_mm)
        state = TaskState(
            task_id="t1", user_id="u1", status=TaskStatus.COMPLETED,
            goal=Goal(request="test learning", success_criteria=["criteria"]),
            updated_at=datetime.now(timezone.utc)
        )

        feedback = {"content": "Good job", "rating": 5}
        reflection = await engine.learn_from_task(state, feedback)

        # Assertions
        assert reflection["patterns"]["confidence_score"] == 1.0
        assert reflection["user_preference_updates"]["preferred_language"] == "Python"

        # Verify interactions with MemoryManager
        mock_mm.update_user_preferences.assert_called_once_with("u1", {"preferred_language": "Python"})
        mock_mm.add_historical_pattern.assert_called_once()

        # Check if historical pattern was created correctly
        called_pattern = mock_mm.add_historical_pattern.call_args[0][0]
        assert called_pattern.user_id == "u1"
        assert called_pattern.task_id == "t1"
        assert called_pattern.success_score == 1.0
        assert called_pattern.approach == "Used direct implementation"
