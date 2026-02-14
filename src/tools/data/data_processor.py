from typing import Any, Dict, List
import pandas as pd
from src.tools.base import BaseTool, ToolMetadata
from src.utils.logger import logger

class DataProcessorTool(BaseTool):
    """Tool for processing and transforming structured data."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="data_processor",
            description="Process and transform structured data using pandas.",
            parameters={
                "type": "object",
                "properties": {
                    "data": {"type": "array", "items": {"type": "object"}, "description": "The data to process"},
                    "operations": {"type": "array", "items": {"type": "object"}, "description": "Transformations to apply"}
                },
                "required": ["data", "operations"]
            },
            returns={"type": "array", "items": {"type": "object"}, "description": "The processed data"}
        )

    async def execute(self, data: List[Dict[str, Any]], operations: List[Dict[str, Any]], **kwargs) -> List[Dict[str, Any]]:
        logger.info(f"Processing data with {len(operations)} operations")
        try:
            df = pd.DataFrame(data)
            # Simulated operations logic
            # In a real implementation, we would safely apply pandas transformations
            return df.to_dict(orient="records")
        except Exception as e:
            logger.error(f"Data processor failed: {str(e)}")
            raise e
