import numpy as np
from typing import List, Dict, Any, Optional
from src.core.types import UserMemory, HistoricalPattern
from src.utils.logger import logger
from src.memory.memory_manager import MemoryManager

# Lazy imports for optional heavy dependencies
_model = None

def get_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model

class SemanticSearch:
    """Provides similarity-based retrieval of past experiences and knowledge using vector embeddings."""

    def __init__(self, memory_manager: Optional[MemoryManager] = None):
        self.model_name = 'all-MiniLM-L6-v2'
        self.memory_manager = memory_manager or MemoryManager()
        logger.info(f"Initialized SemanticSearch with model: {self.model_name}")

    async def find_relevant_patterns(
        self,
        query: str,
        user_id: str,
        limit: int = 3
    ) -> List[HistoricalPattern]:
        """
        Uses sentence-transformers to generate embeddings and queries MongoDB for similar patterns.
        """
        logger.debug(f"Searching for relevant patterns for query: {query}")

        try:
            # 1. Generate query embedding
            query_embedding = self.generate_embedding(query)

            # 2. Search database
            results = await self.memory_manager.search_patterns(
                user_id=user_id,
                query_vector=query_embedding,
                limit=limit
            )

            if not results:
                logger.info("No vector search results found for the query.")

            return results
        except Exception as e:
            logger.error(f"Semantic search failed: {str(e)}")
            return []

    def generate_embedding(self, text: str) -> List[float]:
        """Generates a vector embedding for the given text."""
        model = get_model()
        embedding = model.encode([text])[0]
        return embedding.tolist()
