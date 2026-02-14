from typing import Dict, List, Optional
from src.tools.base_tool import BaseTool
from src.utils.logger import logger

class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}

    def register_tool(self, tool: BaseTool):
        name = tool.metadata.name
        if name in self._tools:
            logger.warning(f"Overwriting existing tool in registry: {name}")
        self._tools[name] = tool
        logger.info(f"Registered tool: {name}")

    def get_tool(self, name: str) -> Optional[BaseTool]:
        return self._tools.get(name)

    def list_tools(self) -> List[str]:
        return list(self._tools.keys())

    def get_tool_metadata_list(self) -> List[Dict[str, Any]]:
        return [tool.metadata.dict() for tool in self._tools.values()]

tool_registry = ToolRegistry()
