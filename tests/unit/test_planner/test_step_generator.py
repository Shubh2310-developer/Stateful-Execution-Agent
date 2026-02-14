import pytest
from unittest.mock import AsyncMock, patch
from src.planner.step_generator import StepGenerator
from src.core.types import UserMemory
from datetime import datetime

@pytest.mark.asyncio
async def test_step_generator_success():
    # Mock response matching the Step schema
    mock_response = """
    {
        "steps": [
            {
                "step_id": "step_001",
                "order": 1,
                "action": "web_search",
                "description": "search something",
                "success_criteria": "found something",
                "tools_needed": ["web_search"]
            }
        ]
    }
    """

    with patch("src.planner.step_generator.groq_client") as mock_groq:
        mock_groq.generate_response = AsyncMock(return_value=mock_response)

        generator = StepGenerator()
        goal = {"primary_objective": "Test objective"}
        result = await generator.generate(goal, ["web_search"])

        assert len(result) == 1
        assert result[0].step_id == "step_001"
        assert result[0].action == "web_search"
        mock_groq.generate_response.assert_called_once()
