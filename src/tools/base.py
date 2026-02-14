from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field

class ToolMetadata(BaseModel):
    name: str
    description: str
    parameters: Dict[str, Any] = Field(default_factory=dict, description="JSON Schema for input parameters")
    returns: Dict[str, Any] = Field(default_factory=dict, description="JSON Schema for return value")
    version: str = "1.0.0"

class BaseTool(ABC):
    """Base interface for all tools in the system."""

    @property
    @abstractmethod
    def metadata(self) -> ToolMetadata:
        """Returns metadata about the tool."""
        pass

    @abstractmethod
    async def execute(self, **kwargs) -> Any:
        """Executes the tool's primary logic."""
        pass

    def validate_input(self, **kwargs) -> bool:
        """Validates the input parameters against the tool's schema."""
        # Implementation using Pydantic or jsonschema could be added here
        # For now, we'll check against the metadata parameters
        required = self.metadata.parameters.get("required", [])
        for field in required:
            if field not in kwargs:
                return False
        return True

    def get_schema(self) -> Dict[str, Any]:
        """Returns the tool's JSON schema for LLM consumption."""
        return {
            "name": self.metadata.name,
            "description": self.metadata.description,
            "parameters": self.metadata.parameters,
        }
