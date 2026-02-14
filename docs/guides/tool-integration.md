# Tool Integration Guide

The Stateful Execution Agent uses a modular tool system that allows it to interact with external APIs, databases, and the filesystem.

## Anatomy of a Tool

Every tool must inherit from `BaseTool` and implement the `metadata` property and `run` method.

```python
from src.tools.base_tool import BaseTool, ToolMetadata

class MyCustomTool(BaseTool):
    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="my_tool",
            description="What this tool does",
            input_schema={"param1": "string"},
            output_type="string"
        )

    async def run(self, param1: str) -> str:
        # Implementation logic
        return f"Processed {param1}"
```

## Registering a Tool

Tools are managed by the `ToolRegistry`. To make a tool available to the agent:

1.  **Place your tool file** in a relevant subdirectory of `src/tools/` (e.g., `src/tools/custom/`).
2.  **Add the tool instance** to the registry in `src/tools/tool_registry.py` or during application startup.

```python
from src.tools.tool_registry import tool_registry
from .my_tool import MyCustomTool

tool_registry.register_tool(MyCustomTool())
```

## Using Tools in Planning

The `Planner` uses the `ToolSelector` to identify which tools match the actions defined in a plan. Ensure your tool name matches the `action` string the LLM is expected to generate.

## Examples

See `examples/custom_tool_integration.py` for a complete example of adding and using a new capability.
