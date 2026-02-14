from typing import Any, Dict, List, Optional
from pydantic import BaseModel

class UserPreferences:
    """Stores explicit and learned user preferences."""
    document_tone: str = "professional"
    detail_level: str = "medium"
    preferred_formats: List[str] = ["markdown", "pdf"]
    formatting_rules: Dict[str, Any] = {}

    def update_preference(self, key: str, value: Any):
        if hasattr(self, key):
            setattr(self, key, value)
        else:
            self.formatting_rules[key] = value
