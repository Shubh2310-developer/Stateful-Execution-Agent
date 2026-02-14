import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from src.reviewer.reviewer import Reviewer
from src.core.types import TaskState, Artifact, Goal, TaskStatus
from datetime import datetime

@pytest.mark.asyncio
async def test_reviewer_approved():
    reviewer = Reviewer()

    state = TaskState(
        task_id="t1",
        user_id="u1",
        status=TaskStatus.COMPLETED,
        goal=Goal(request="test", success_criteria=["criteria"]),
        current_step_index=1,
        artifacts=[
            Artifact(
                id="art1", task_id="t1", step_id="s1",
                type="document", uri="file:///tmp/1.md",
                created_at=datetime.utcnow()
            )
        ]
    )
    # Mock steps for achievement ratio
    state.plan = MagicMock()
    state.plan.steps = [MagicMock()]

    with patch.object(reviewer.artifact_manager, "get_artifact_content", return_value="# Content"), \
         patch.object(reviewer.quality_checker, "check_quality", return_value={"quality_score": 0.9}), \
         patch("src.reviewer.reviewer.groq_client") as mock_groq:

        mock_groq.generate_response = AsyncMock(return_value='{"overall_success": true, "quality_score": 0.9, "feedback": "Good", "reasoning": "Test reasoning"}')

        result = await reviewer.review_task(state)

        assert result["overall_success"] is True
        assert result["quality_score"] == 0.9
        assert "art1" in result["artifact_quality"]
