from typing import Any, Dict, List, Optional
from src.tools.base import BaseTool, ToolMetadata
from src.utils.logger import logger

class DocumentGeneratorTool(BaseTool):
    """Tool for generating structured markdown documents."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="document_generator",
            description=(
                "Creates well-formatted markdown documents with sections and headings. "
                "USE THIS TOOL FOR: Writing documentation, creating reports, generating formatted text files. "
                "DO NOT USE FOR: Searching information, writing code, performing calculations. "
                "REQUIRES: Pre-defined content for each section."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "The document title"},
                    "sections": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "heading": {"type": "string", "description": "Section heading"},
                                "content": {"type": "string", "description": "Section content/body"}
                            },
                            "required": ["heading", "content"]
                        },
                        "description": "List of sections with headings and content"
                    },
                    "tone": {"type": "string", "description": "Writing tone: professional, casual, technical", "default": "professional"}
                },
                "required": ["title", "sections"]
            },
            returns={"type": "string", "description": "The generated markdown document"}
        )

    async def execute(self, title: str, sections: List[Dict[str, Any]], tone: str = "professional", **kwargs) -> str:
        logger.info(f"Generating document: {title} with tone: {tone}")

        doc = f"# {title}\n\n"
        for section in sections:
            doc += f"## {section.get('heading', 'Section')}\n"
            doc += f"{section.get('content', '')}\n\n"

        return doc
