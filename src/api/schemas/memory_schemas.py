from typing import Any, Dict, List, Optional
from pydantic import BaseModel
from datetime import datetime

class UserMemoryResponse(BaseModel):
    user_id: str
    profile: Dict[str, Any]
    preferences: Dict[str, Any]
    domain_knowledge: Dict[str, Any]
    historical_patterns: List[Dict[str, Any]]
    last_updated: datetime

class PreferenceUpdate(BaseModel):
    updates: Dict[str, Any]
