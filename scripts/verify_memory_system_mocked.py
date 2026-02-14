import asyncio
import os
import sys
import numpy as np
from datetime import datetime
from uuid import uuid4
from unittest.mock import MagicMock, AsyncMock, patch, ANY

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.core.types import TaskState, Goal, TaskStatus, UserMemory, UserProfile, UserPreferences, Plan, Step, HistoricalPattern
from src.orchestration.workflow_engine import WorkflowEngine
from src.memory.memory_manager import MemoryManager
from src.memory.retrieval.semantic_search import SemanticSearch
from src.memory.learning.adaptation_engine import AdaptationEngine
from src.utils.logger import logger

class AsyncIterator:
    def __init__(self, items):
        self.items = items
        self.index = 0

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.index >= len(self.items):
            raise StopAsyncIteration
        item = self.items[self.index]
        self.index += 1
        return item

async def verify_memory_system_mocked():
    logger.info("Starting MOCKED Memory System Verification...")

    user_id = "test_user_123"

    # 1. Mock Database and LLM
    mock_profiles = AsyncMock()

    # Mock User Memory
    initial_memory = UserMemory(
        user_id=user_id,
        profile=UserProfile(user_id=user_id, role="Tester"),
        preferences=UserPreferences(document_tone="casual", detail_level="low")
    )

    # Setup mock return values
    mock_profiles.find_one.return_value = initial_memory.dict()

    with patch("src.memory.memory_manager.AsyncIOMotorClient"), \
         patch("src.memory.learning.adaptation_engine.groq_client.generate_response", new_callable=AsyncMock) as mock_groq, \
         patch("src.memory.retrieval.semantic_search.get_model") as mock_get_model:

        # Setup mocks
        mock_groq.return_value = '{"reasoning": "The user wants more professional output.", "lessons_learned": ["Always use professional tone for architecture summaries"], "user_preferences": {"document_tone": "professional"}, "historical_pattern": {"task_type": "Architecture Summary", "approach": "Identify components, explain interactions, use formal language.", "success_score": 0.9}}'

        mock_model = MagicMock()
        # SentenceTransformer.encode returns numpy array
        mock_model.encode.return_value = np.array([[0.1] * 384])
        mock_get_model.return_value = mock_model

        # Initialize components with mocked DB
        memory_manager = MemoryManager()
        memory_manager.profiles = mock_profiles

        # Mock patterns collection
        mock_patterns = MagicMock()
        memory_manager.patterns = mock_patterns
        mock_patterns.insert_one = AsyncMock()

        adaptation_engine = AdaptationEngine(memory_manager=memory_manager)

        workflow = WorkflowEngine()
        workflow.adaptation_engine = adaptation_engine

        # 2. Simulate a Completed Task
        state = TaskState(
            task_id=f"task_{uuid4().hex[:8]}",
            user_id=user_id,
            goal=Goal(
                request="Create a professional summary of the project architecture",
                success_criteria=["Architecture summary produced", "Tone is professional"]
            ),
            status=TaskStatus.COMPLETED,
            plan=Plan(
                task_id="t1",
                steps=[
                    Step(step_id="s1", action="summarize", description="Summarizing architecture", status=TaskStatus.COMPLETED)
                ]
            ),
            metadata={"user_feedback": {"tone_correction": "Please use a more professional tone next time", "rating": 5}}
        )

        logger.info("Triggering learning loop...")
        await workflow.process_task(state, available_tools=["summarize"], user_memory=initial_memory)

        # 3. Verify Interactions

        # Verify preferences update was called
        mock_profiles.update_one.assert_any_call(
            {"user_id": user_id},
            {"$set": {"preferences.document_tone": "professional", "last_updated": ANY}}
        )
        logger.info("Verified: User preferences update was triggered with 'professional' tone.")

        # Verify historical pattern was saved
        mock_patterns.insert_one.assert_called_once()
        saved_pattern_args = mock_patterns.insert_one.call_args[0][0]
        assert saved_pattern_args["user_id"] == user_id
        assert saved_pattern_args["goal_request"] == state.goal.request
        assert "Identify components" in saved_pattern_args["approach"]
        logger.info("Verified: Historical pattern was saved to database.")

        # 4. Verify Semantic Retrieval
        semantic_search = SemanticSearch(memory_manager)

        # Setup mock retrieval
        mock_cursor = MagicMock()
        mock_cursor.__aiter__ = lambda x: AsyncIterator([saved_pattern_args])
        mock_patterns.aggregate.return_value = mock_cursor

        logger.info("Testing semantic retrieval for similar goal...")
        query = "Summarize technical architecture"
        results = await semantic_search.find_relevant_patterns(query, user_id=user_id, limit=1)

        if results and results[0].goal_request == state.goal.request:
            logger.info(f"Successfully retrieved relevant pattern: {results[0].goal_request}")
            logger.info(f"Approach learned: {results[0].approach}")
        else:
            logger.error(f"Semantic retrieval failed. Results: {results}")

    logger.info("MOCKED Memory System Verification Successful.")

if __name__ == "__main__":
    asyncio.run(verify_memory_system_mocked())
