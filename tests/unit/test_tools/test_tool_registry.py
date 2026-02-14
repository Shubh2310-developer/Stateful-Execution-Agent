import pytest
from src.tools.tool_registry import ToolRegistry
from src.tools.base_tool import BaseTool, ToolMetadata

class MockTool(BaseTool):
    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="mock_tool",
            description="A mock tool for testing",
            input_schema={"param": "string"},
            output_type="string"
        )
    async def run(self, param: str) -> str:
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

    # Test metadata list
    metadata_list = registry.get_tool_metadata_list()
    assert len(metadata_list) == 1
    assert metadata_list[0]["name"] == "mock_tool"

def test_get_nonexistent_tool():
    registry = ToolRegistry()
    assert registry.get_tool("invalid") is None
