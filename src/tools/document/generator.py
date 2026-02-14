from typing import Any, Dict, Optional
from src.tools.base_tool import BaseTool, ToolMetadata
from src.utils.logger import logger

class DocumentGeneratorTool(BaseTool):
    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="document_generator",
            description="Generate structured markdown documents from outlines and content segments.",
            input_schema={
                "title": "string",
                "sections": "array",
                "tone": "string"
            },
            output_type="string"
        )

    async def run(self, title: str, sections: list, tone: str = "professional") -> str:
        logger.info(f"Generating document: {title}")

        doc = f"# {title}\n\n"
        for section in sections:
            doc += f"## {section.get('heading', 'Section')}\n"
            doc += f"{section.get('content', '')}\n\n"

        return doc
