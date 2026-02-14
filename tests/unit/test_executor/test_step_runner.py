import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from src.executor.step_runner import StepRunner
from src.core.types import Step, Artifact
from datetime import datetime

@pytest.mark.asyncio
async def test_run_step_success():
    # Mock dependencies
    mock_artifact_manager = MagicMock()
    mock_artifact_manager.get_artifact_content.return_value = {"prev": "data"}

    # Mock LLM response for tool parameters
    mock_llm_response = """
    {
        "action": "web_search",
        "parameters": {"query": "test query"},
        "reasoning": "Need to search for test data",
        "confidence": 0.95
    }
    """

    # Mock Tool execution result
    mock_tool_result = {"results": ["found something"]}

    with patch("src.executor.step_runner.groq_client") as mock_groq:
        mock_groq.generate_response = AsyncMock(return_value=mock_llm_response)

        runner = StepRunner(mock_artifact_manager)

        # Patch tool orchestrator
        runner.tool_orchestrator.invoke_tool = AsyncMock(return_value=mock_tool_result)

        # Patch artifact manager create_artifact
        mock_artifact_manager.create_artifact = AsyncMock(return_value=Artifact(
            id="art_1", task_id="t1", step_id="s1", type="data",
            uri="file:///tmp/1.json", created_at=datetime.utcnow()
        ))

        step = Step(
            step_id="step_001", order=1, action="web_search",
            description="search test", success_criteria="found results"
        )

        result = await runner.run_step("task_001", step, {})

        assert result["status"] == "completed"
        assert result["artifact"].id == "art_1"
        assert result["decision"].choice_made == "web_search"
        assert result["decision"].confidence == 0.95

        runner.tool_orchestrator.invoke_tool.assert_called_once_with("web_search", {"query": "test query"})
