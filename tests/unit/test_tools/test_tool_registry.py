import pytest
from src.tools.tool_registry import ToolRegistry
from src.tools.base import BaseTool, ToolMetadata

class MockTool(BaseTool):
    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="mock_tool",
            description="A mock tool for testing",
            parameters={
                "type": "object",
                "properties": {
                    "param": {"type": "string"}
                },
                "required": ["param"]
            },
            returns={"type": "string"}
        )
    async def execute(self, param: str, **kwargs) -> str:
        return f"result_{param}"

def test_tool_registry_operations():
    registry = ToolRegistry()
    tool = MockTool()

    # Test registration
    registry.register_tool(tool)
    assert "mock_tool" in registry.list_tools()

    # Test retrieval
    retrieved = registry.get_tool("mock_tool")
    assert retrieved == tool

    # Test schemas
    schemas = registry.get_tool_schemas()
    assert len(schemas) == 1
    assert schemas[0]["name"] == "mock_tool"
    assert "parameters" in schemas[0]

def test_get_nonexistent_tool():
    registry = ToolRegistry()
    assert registry.get_tool("invalid") is None
