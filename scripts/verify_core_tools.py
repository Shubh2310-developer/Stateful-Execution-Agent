import asyncio
import sys
import os

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.tools.document.summarizer import SummarizerTool
from src.tools.document.search import DocumentSearchTool
from src.core.types import Artifact, UserMemory
from src.utils.logger import logger

async def test_summarizer():
    print("\n--- Testing Summarizer Tool ---")
    tool = SummarizerTool()

    # Test small text
    small_text = "The quick brown fox jumps over the lazy dog. This is a test of the summarization system."
    result = await tool.execute(text=small_text)
    print(f"Small text result: {result['content'][:100]}...")

    # Test large text (simulated)
    large_text = "Important data point. " * 1000 # ~22,000 chars, should trigger chunking
    result = await tool.execute(text=large_text, chunk_size=5000)
    print(f"Large text metadata: {result['metadata']}")
    print(f"Large text summary length: {len(result['content'])}")

async def test_search():
    print("\n--- Testing Document Search Tool ---")
    tool = DocumentSearchTool()

    mock_artifacts = [
        Artifact(
            id="art_1",
            task_id="task_123",
            type="document",
            uri="file:///tmp/test.txt",
            metadata={"title": "Project Alpha Report", "tags": ["confidential"]}
        ),
        Artifact(
            id="art_2",
            task_id="task_123",
            type="data",
            uri="file:///tmp/data.json",
            metadata={"description": "Financial metrics for Q4"}
        )
    ]

    # Search artifacts
    result = await tool.execute(query="Alpha Report", scope="artifacts", available_artifacts=mock_artifacts)
    print(f"Search results count: {len(result['results'])}")
    if result['results']:
        print(f"First result: {result['results'][0]['artifact_id']}")

if __name__ == "__main__":
    # Mocking groq_client to avoid actual API calls in this verification script
    # if you want to run it for real, ensure GROQ_API_KEY is set.
    if not os.getenv("GROQ_API_KEY"):
        print("Skipping LLM-dependent tests (GROQ_API_KEY not set)")
        # We can still test the logic that doesn't depend on LLM response content

    asyncio.run(test_search())
    # asyncio.run(test_summarizer()) # Requires LLM
