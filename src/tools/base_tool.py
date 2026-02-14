from abc import ABC, abstractmethod
from typing import Any, Dict, List
from pydantic import BaseModel

class ToolMetadata(BaseModel):
    name: str
    description: str
    input_schema: Dict[str, Any]
    output_type: str

class BaseTool(ABC):
    @property
    @abstractmethod
    def metadata(self) -> ToolMetadata:
        pass

    @abstractmethod
    async def run(self, **kwargs) -> Any:
        pass
