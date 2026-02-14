import asyncio
from src.tools.base_tool import BaseTool, ToolMetadata
from src.tools.tool_registry import tool_registry
from src.utils.logger import logger

class WeatherTool(BaseTool):
    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="get_weather",
            description="Fetch the current weather for a specific city.",
            input_schema={
                "city": "string"
            },
            output_type="string"
        )

    async def run(self, city: str) -> str:
        logger.info(f"Fetching weather for {city}...")
        # Simulated weather API
        return f"The weather in {city} is currently Sunny, 22°C."

def register_custom_tools():
    weather_tool = WeatherTool()
    tool_registry.register_tool(weather_tool)
    print(f"Custom tool '{weather_tool.metadata.name}' registered.")

if __name__ == "__main__":
    register_custom_tools()
    print("Available tools:", tool_registry.list_tools())
