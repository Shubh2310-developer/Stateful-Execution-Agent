from typing import List, Dict, Any, Optional
from src.core.types import UserMemory
from src.utils.logger import logger

class SemanticSearch:
    """Provides similarity-based retrieval of past experiences and knowledge."""

    async def find_relevant_patterns(
        self,
        query: str,
        memory: UserMemory,
        limit: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Simple keyword-based relevance for now.
        Future: Use sentence-transformers for real semantic search.
        """
        logger.debug(f"Searching for relevant patterns for query: {query}")
        patterns = memory.historical_patterns
        if not patterns:
            return []

        # Simple case-insensitive keyword match on 'task_type' or 'description'
        query_words = query.lower().split()
        scored_patterns = []

        for p in patterns:
            score = 0
            text_to_search = (p.get("task_type", "") + " " + p.get("approach", "")).lower()
            for word in query_words:
                if word in text_to_search:
                    score += 1

            if score > 0:
                scored_patterns.append((score, p))

        # Sort by score descending
        scored_patterns.sort(key=lambda x: x[0], reverse=True)

        return [p for score, p in scored_patterns[:limit]]
