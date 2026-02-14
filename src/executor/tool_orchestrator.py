from typing import Any, Dict, List, Optional
from src.tools.tool_selector import ToolSelector
from src.core.exceptions import ToolError
from src.utils.logger import logger

class ToolOrchestrator:
    """Orchestrates the selection and invocation of tools for plan steps."""

    def __init__(self):
        self.tool_selector = ToolSelector()

    async def invoke_tool(self, action: str, parameters: Dict[str, Any]) -> Any:
        logger.info(f"Invoking tool for action: {action}")

        tool = self.tool_selector.select_tool(action)
        if not tool:
            raise ToolError(f"No tool found for action: {action}")

        try:
            # Validate input parameters against tool schema (simplified for now)
            logger.debug(f"Executing {action} with params: {parameters}")
            result = await tool.run(**parameters)
            logger.info(f"Tool {action} completed successfully.")
            return result
        except Exception as e:
            logger.error(f"Error in tool {action}: {str(e)}")
            raise ToolError(f"Tool invocation failed: {str(e)}")
