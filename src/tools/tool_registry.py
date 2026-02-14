import importlib
import inspect
import os
import pkgutil
from typing import Any, Dict, List, Optional, Type
from src.tools.base import BaseTool
from src.utils.logger import logger

class ToolRegistry:
    """Registry for managing and discovering agent tools."""

    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}

    def register_tool(self, tool: BaseTool):
        """Manually register a tool instance."""
        name = tool.metadata.name
        if name in self._tools:
            logger.warning(f"Overwriting existing tool in registry: {name}")
        self._tools[name] = tool
        logger.info(f"Registered tool: {name}")

    def get_tool(self, name: str) -> Optional[BaseTool]:
        """Retrieve a tool by name."""
        return self._tools.get(name)

    def list_tools(self) -> List[str]:
        """List names of all registered tools."""
        return list(self._tools.keys())

    def get_tool_schemas(self) -> List[Dict[str, Any]]:
        """Return JSON schemas for all registered tools for LLM consumption."""
        return [tool.get_schema() for tool in self._tools.values()]

    def discover_tools(self, package_path: str = "src.tools"):
        """
        Automatically discovers and registers tools in the specified package.
        Looks for subclasses of BaseTool.
        """
        logger.info(f"Starting tool discovery in {package_path}")

        # Get the actual file path of the package
        try:
            package = importlib.import_module(package_path)
        except ImportError as e:
            logger.error(f"Failed to import tool package {package_path}: {str(e)}")
            return

        package_dir = os.path.dirname(package.__file__)

        # Iterate through all submodules
        for _, name, is_pkg in pkgutil.walk_packages([package_dir], package_path + "."):
            if name == "src.tools.base" or name == "src.tools.base_tool":
                continue
            try:
                module = importlib.import_module(name)
                for _, obj in inspect.getmembers(module):
                    if (inspect.isclass(obj) and
                        issubclass(obj, BaseTool) and
                        obj is not BaseTool and
                        not inspect.isabstract(obj)):

                        try:
                            # Instantiate and register
                            tool_instance = obj()
                            self.register_tool(tool_instance)
                        except Exception as e:
                            logger.error(f"Failed to instantiate tool {obj.__name__}: {str(e)}")
            except Exception as e:
                logger.error(f"Error loading module {name}: {str(e)}")

# Global instance for easy access
tool_registry = ToolRegistry()
