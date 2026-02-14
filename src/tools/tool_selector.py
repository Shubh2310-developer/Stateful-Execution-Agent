from typing import List, Optional
from src.tools.tool_registry import tool_registry
from src.tools.base_tool import BaseTool
from src.utils.logger import logger

class ToolSelector:
    @staticmethod
    def select_tool(step_action: str) -> Optional[BaseTool]:
        """
        Simple tool selector that matches step action to registered tool names.
        In a more advanced version, this could use LLM or semantic search.
        """
        logger.debug(f"Selecting tool for action: {step_action}")

        # Exact match
        tool = tool_registry.get_tool(step_action)
        if tool:
            return tool

        # Partial match or fallback logic could go here
        logger.warning(f"No exact tool match found for action: {step_action}")
        return None

    @staticmethod
    def get_available_tool_names() -> List[str]:
        return tool_registry.list_tools()
