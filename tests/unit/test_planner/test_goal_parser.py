import pytest
from unittest.mock import AsyncMock, patch
from src.planner.goal_parser import GoalParser

@pytest.mark.asyncio
async def test_goal_parser_success():
    # Mock the groq_client response
    mock_response = '{"primary_objective": "Create a Python script", "success_criteria": ["criteria1"], "priority": "high"}'

    with patch("src.planner.goal_parser.groq_client") as mock_groq:
        mock_groq.generate_response = AsyncMock(return_value=mock_response)

        parser = GoalParser()
        result = await parser.parse("Write a hello world script")

        assert result["primary_objective"] == "Create a Python script"
        assert result["priority"] == "high"
        assert "success_criteria" in result
        mock_groq.generate_response.assert_called_once()
