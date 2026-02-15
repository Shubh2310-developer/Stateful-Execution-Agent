from typing import Any, Dict, List, Optional
from src.tools.tool_selector import ToolSelector
from src.core.exceptions import ToolError, ExecutionError, ValidationError
from src.utils.logger import logger

class ToolOrchestrator:
    """Orchestrates the selection and invocation of tools for plan steps."""

    def __init__(self):
        self.tool_selector = ToolSelector()

    async def invoke_tool(self, action: str, parameters: Dict[str, Any], **kwargs) -> Any:
        """
        Selects, validates, and executes a tool based on the action name.
        """
        logger.info(f"Invoking tool for action: {action}")

        # Debug: Check what tools are available
        available_tools = self.tool_selector.get_available_tool_names()
        logger.debug(f"Available tools: {available_tools}")
        
        tool = self.tool_selector.select_tool(action)
        if not tool:
            logger.error(f"Tool not found: {action}. Available: {available_tools}")
            
            # Try direct registry access as fallback
            from src.tools.tool_registry import tool_registry
            direct_tool = tool_registry.get_tool(action)
            if direct_tool:
                logger.info(f"Found tool via direct registry access: {action}")
                tool = direct_tool
            else:
                raise ToolError(f"No tool found for action: {action}. Available: {available_tools}")
        
        if not tool:
            raise ToolError(f"No tool found for action: {action}")

        # 1. Validate Input
        if not tool.validate_input(**parameters):
            logger.error(f"Input validation failed for tool {action}. Params: {parameters}")
            raise ValidationError(f"Invalid parameters for tool {action}")

        # 2. Execute
        try:
            logger.debug(f"Executing {action} with params: {parameters}")
            # Use execute() as defined in the new BaseTool interface
            # Pass extra context via kwargs
            result = await tool.execute(**parameters, **kwargs)
            logger.info(f"Tool {action} completed successfully.")
            return result
        except Exception as e:
            logger.error(f"Error executing tool {action}: {str(e)}")
            # Wrap in ExecutionError to prevent the whole agent from failing
            raise ExecutionError(f"Tool execution failed for action '{action}': {str(e)}", details={"action": action, "parameters": parameters})
