from typing import Any, Dict, List, Optional
from pydantic import BaseModel

class DomainKnowledge:
    """Represents learned domain-specific facts and concepts."""
    concepts: Dict[str, str] = {}
    relationships: List[Dict[str, Any]] = []

    def add_fact(self, concept: str, description: str):
        self.concepts[concept] = description

    def get_fact(self, concept: str) -> Optional[str]:
        return self.concepts.get(concept)
