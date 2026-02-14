from typing import Any, Dict, List, Optional
from pydantic import BaseModel

class UserProfile(BaseModel):
    """Represents a user's identity, role, and persistent attributes."""
    user_id: str
    role: Optional[str] = None
    company: Optional[str] = None
    industry: Optional[str] = None
    communication_style: str = "professional"
    technical_depth: str = "medium"

class UserPreferences(BaseModel):
    """Stores explicit and learned user preferences."""
    document_tone: str = "professional"
    detail_level: str = "medium"
    preferred_formats: List[str] = ["markdown", "pdf"]
    formatting_rules: Dict[str, Any] = {}
