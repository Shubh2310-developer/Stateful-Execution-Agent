from typing import List, Optional
from src.tools.tool_registry import tool_registry
from src.tools.base import BaseTool
from src.utils.logger import logger

class ToolSelector:
    def __init__(self):
        self.tool_registry = tool_registry
    
    def select_tool(self, step_action: str) -> Optional[BaseTool]:
        """
        Simple tool selector that matches step action to registered tool names.
        In a more advanced version, this could use LLM or semantic search.
        """
        logger.debug(f"Selecting tool for action: {step_action}")

        # Exact match
        tool = self.tool_registry.get_tool(step_action)
        if tool:
            return tool

        # Try to map common action names to actual tools
        action_mapping = {
            'google_search': 'web_search',
            'document_search': 'document_search',  
            'search': 'web_search',
            'calculate': 'calculator',
            'generate_document': 'document_generator',
            'create_document': 'document_generator',
            'write_file': 'file_writer',
            'save_file': 'file_writer'
        }
        
        if step_action in action_mapping:
            mapped_action = action_mapping[step_action]
            logger.info(f"Mapped action '{step_action}' to '{mapped_action}'")
            tool = self.tool_registry.get_tool(mapped_action)
            if tool:
                return tool

        # Partial match or fallback logic could go here
        logger.warning(f"No exact tool match found for action: {step_action}")
        return None

    def get_available_tool_names(self) -> List[str]:
        return self.tool_registry.list_tools()
