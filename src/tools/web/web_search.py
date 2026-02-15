from typing import Any, Dict, List
from src.tools.base import BaseTool, ToolMetadata
from src.utils.logger import logger

class WebSearchTool(BaseTool):
    """Tool for searching the web for information."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="web_search",
            description=(
                "Searches the internet for current information, facts, and resources. "
                "USE THIS TOOL FOR: Finding information online, researching topics, looking up facts, getting current data. "
                "DO NOT USE FOR: Creating content, writing code, performing calculations. "
                "RETURNS: List of search results with titles, URLs, and snippets."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The search query or keywords to search for"},
                    "max_results": {"type": "integer", "description": "Maximum number of results to return (1-10)", "default": 5}
                },
                "required": ["query"]
            },
            returns={"type": "array", "items": {"type": "object"}, "description": "List of search results with title, url, and snippet"}
        )

    async def execute(self, query: str, max_results: int = 5, **kwargs) -> List[Dict[str, Any]]:
        logger.info(f"Searching the web for: {query}")

        # In a real implementation, this would call a Search API (Serper, Tavily, etc.)
        # For this skeleton, we'll return a simulated response
        return [
            {
                "title": f"Result for {query} 1",
                "url": "https://example.com/1",
                "snippet": f"This is a simulated search result for the query: {query}"
            },
            {
                "title": f"Result for {query} 2",
                "url": "https://example.com/2",
                "snippet": "Another snippet containing relevant information."
            }
        ]
