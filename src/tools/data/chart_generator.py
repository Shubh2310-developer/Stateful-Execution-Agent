from typing import Any, Dict, List
from src.tools.base_tool import BaseTool, ToolMetadata
from src.utils.logger import logger

class ChartGeneratorTool(BaseTool):
    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="chart_generator",
            description="Generate chart specifications (Vega-Lite) from data.",
            input_schema={
                "data": "array",
                "chart_type": "string",
                "x_axis": "string",
                "y_axis": "string"
            },
            output_type="object"
        )

    async def run(self, data: List[Dict[str, Any]], chart_type: str = "bar", **kwargs) -> Dict[str, Any]:
        logger.info(f"Generating {chart_type} chart spec")
        return {
            "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
            "description": f"A {chart_type} chart.",
            "data": {"values": data},
            "mark": chart_type,
            "encoding": {
                "x": {"field": kwargs.get("x_axis"), "type": "nominal"},
                "y": {"field": kwargs.get("y_axis"), "type": "quantitative"}
            }
        }
