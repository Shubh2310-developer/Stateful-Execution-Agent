from typing import Any, Dict, List
from src.tools.base import BaseTool, ToolMetadata
from src.utils.logger import logger

class ChartGeneratorTool(BaseTool):
    """Tool for generating chart specifications."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="chart_generator",
            description="Generate chart specifications (Vega-Lite) from data.",
            parameters={
                "type": "object",
                "properties": {
                    "data": {"type": "array", "items": {"type": "object"}, "description": "The data to visualize"},
                    "chart_type": {"type": "string", "description": "Type of chart (e.g., 'bar', 'line', 'point')", "default": "bar"},
                    "x_axis": {"type": "string", "description": "Field name for X axis"},
                    "y_axis": {"type": "string", "description": "Field name for Y axis"}
                },
                "required": ["data", "x_axis", "y_axis"]
            },
            returns={"type": "object", "description": "Vega-Lite chart specification"}
        )

    async def execute(self, data: List[Dict[str, Any]], chart_type: str = "bar", x_axis: str = None, y_axis: str = None, **kwargs) -> Dict[str, Any]:
        logger.info(f"Generating {chart_type} chart spec")
        return {
            "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
            "description": f"A {chart_type} chart.",
            "data": {"values": data},
            "mark": chart_type,
            "encoding": {
                "x": {"field": x_axis, "type": "nominal"},
                "y": {"field": y_axis, "type": "quantitative"}
            }
        }
