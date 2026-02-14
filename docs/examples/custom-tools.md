# Example: Custom Tool Integration

This example demonstrates how to extend the agent's capabilities by adding a custom tool.

## Scenario: Adding a Weather Lookup Tool

If you want the agent to be able to check the weather, you can create a `WeatherTool`.

### 1. Implement the Tool

Create a new file `src/tools/custom/weather_tool.py`:

```python
from src.tools.base_tool import BaseTool, ToolMetadata
import httpx

class WeatherTool(BaseTool):
    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="get_weather",
            description="Fetch current weather data for a city.",
            input_schema={"city": "string"},
            output_type="string"
        )

    async def run(self, city: str) -> str:
        # Example using a placeholder weather API
        return f"The weather in {city} is currently Sunny, 24°C."
```

### 2. Register the Tool

Update your application entry point to register the new tool:

```python
from src.tools.tool_registry import tool_registry
from src.tools.custom.weather_tool import WeatherTool

tool_registry.register_tool(WeatherTool())
```

### 3. Use in a Task

Now, when you create a task that requires weather information, the Planner will identify the `get_weather` tool as a valid capability.

**Request:**
```json
{
  "user_id": "usr_123",
  "goal": "Check the weather in London and write a short travel recommendation."
}
```

**Generated Plan:**
1. `get_weather` (city="London")
2. `document_generator` (Generate recommendation based on weather)
```
