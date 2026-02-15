from typing import Any, Dict
import os
from pathlib import Path
from src.tools.base import BaseTool, ToolMetadata
from src.utils.logger import logger

class FileWriterTool(BaseTool):
    """Tool for writing content to files."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="file_writer",
            description=(
                "Writes content to files on the filesystem. "
                "USE THIS TOOL FOR: Saving generated code, creating config files, writing data to disk. "
                "DO NOT USE FOR: Generating content, searching information, performing calculations. "
                "RETURNS: Path to the created file."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "filename": {"type": "string", "description": "Name of the file to create (e.g., 'script.py', 'data.json')"},
                    "content": {"type": "string", "description": "Content to write to the file"},
                    "overwrite": {"type": "boolean", "description": "Whether to overwrite if file exists", "default": False}
                },
                "required": ["filename", "content"]
            },
            returns={"type": "string", "description": "Path to the created file"}
        )

    async def execute(self, filename: str, content: str, overwrite: bool = False, **kwargs) -> str:
        logger.info(f"Writing to file: {filename}")

        # Use data/artifacts for file storage
        artifacts_dir = Path("data/artifacts")
        artifacts_dir.mkdir(parents=True, exist_ok=True)
        
        # Extract task_id from kwargs if available
        task_id = kwargs.get('task_id', 'general')
        task_dir = artifacts_dir / task_id
        task_dir.mkdir(exist_ok=True)
        
        file_path = task_dir / filename

        # Check if file exists
        if file_path.exists() and not overwrite:
            raise FileExistsError(f"File {filename} already exists. Set overwrite=True to replace it.")

        # Write content to file
        file_path.write_text(content, encoding='utf-8')
        
        logger.info(f"Successfully wrote {len(content)} characters to {file_path}")
        return str(file_path)
