import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from src.executor.tool_orchestrator import ToolOrchestrator
from src.core.exceptions import ToolError

@pytest.mark.asyncio
async def test_invoke_tool_success():
    orchestrator = ToolOrchestrator()

    mock_tool = MagicMock()
    mock_tool.run = AsyncMock(return_value="tool output")

    with patch.object(orchestrator.tool_selector, "select_tool", return_value=mock_tool):
        result = await orchestrator.invoke_tool("test_tool", {"param": "val"})

        assert result == "tool output"
        mock_tool.run.assert_called_once_with(param="val")

@pytest.mark.asyncio
async def test_invoke_tool_not_found():
    orchestrator = ToolOrchestrator()

    with patch.object(orchestrator.tool_selector, "select_tool", return_value=None):
        with pytest.raises(ToolError, match="No tool found for action: invalid_tool"):
            await orchestrator.invoke_tool("invalid_tool", {})
