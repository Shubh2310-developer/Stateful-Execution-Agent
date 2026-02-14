import pytest
from src.memory.retrieval.semantic_search import SemanticSearch
from src.core.types import UserMemory
from datetime import datetime

@pytest.mark.asyncio
async def test_find_relevant_patterns():
    search = SemanticSearch()

    memory = UserMemory(
        user_id="u1",
        profile={},
        preferences={},
        historical_patterns=[
            {"task_type": "coding", "approach": "use python", "success_score": 0.9},
            {"task_type": "research", "approach": "web search", "success_score": 0.8},
            {"task_type": "coding", "approach": "use javascript", "success_score": 0.7}
        ]
    )

    # Search for coding patterns
    results = await search.find_relevant_patterns("coding task", memory)

    assert len(results) == 2
    assert results[0]["task_type"] == "coding"
    assert "python" in results[0]["approach"] or "javascript" in results[0]["approach"]

    # Search for something not present
    results = await search.find_relevant_patterns("cooking", memory)
    assert len(results) == 0
