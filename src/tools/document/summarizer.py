from typing import Any, Dict
from src.tools.base_tool import BaseTool, ToolMetadata
from src.utils.logger import logger

class SummarizerTool(BaseTool):
    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="summarizer",
            description="Summarize long text or documents into key points.",
            input_schema={
                "text": "string",
                "max_length": "integer"
            },
            output_type="string"
        )

    async def run(self, text: str, max_length: int = 500) -> str:
        logger.info(f"Summarizing text of length {len(text)}")
        # In a real impl, this would call an LLM with a summarization prompt
        return text[:max_length] + "..."
