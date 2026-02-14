from typing import Any, Dict, List
from src.tools.base_tool import BaseTool, ToolMetadata
from src.utils.logger import logger

class DocumentSearchTool(BaseTool):
    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="document_search",
            description="Search internal knowledge base and previous artifacts.",
            input_schema={
                "query": "string",
                "scope": "string"
            },
            output_type="list"
        )

    async def run(self, query: str, scope: str = "all") -> List[Dict[str, Any]]:
        logger.info(f"Searching documents for: {query} in scope: {scope}")

        # Simulated search results
        return [
            {
                "id": "doc_001",
                "title": "Previous Report",
                "content": "Relevant content snippet about " + query
            }
        ]
