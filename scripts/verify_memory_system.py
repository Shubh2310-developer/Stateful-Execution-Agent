import asyncio
import os
import sys
from datetime import datetime
from uuid import uuid4

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.core.types import TaskState, Goal, TaskStatus, UserMemory, UserProfile, UserPreferences, Plan, Step
from src.orchestration.workflow_engine import WorkflowEngine
from src.memory.memory_manager import MemoryManager
from src.memory.retrieval.semantic_search import SemanticSearch
from src.utils.logger import logger

async def verify_memory_system():
    logger.info("Starting Memory System Verification...")

    # 1. Setup Mock User Memory
    user_id = f"test_user_{uuid4().hex[:4]}"
    memory_manager = MemoryManager()

    initial_memory = UserMemory(
        user_id=user_id,
        profile=UserProfile(user_id=user_id, role="Tester"),
        preferences=UserPreferences(document_tone="casual", detail_level="low")
    )
    await memory_manager.save_user_memory(initial_memory)
    logger.info(f"Initialized mock user memory for {user_id}")

    # 2. Simulate a Completed Task
    workflow = WorkflowEngine()

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

    # 3. Trigger Workflow (which now includes learning)
    # We manually set status to COMPLETED to trigger the learning loop in process_task
    # or we can call learn_from_task directly.
    # process_task in workflow_engine triggers learning if status is COMPLETED.
    logger.info("Triggering learning loop via WorkflowEngine...")
    await workflow.process_task(state, available_tools=["summarize"], user_memory=initial_memory)

    # 4. Verify Preferences Update
    updated_memory = await memory_manager.get_user_memory(user_id)
    logger.info(f"Updated preferences: {updated_memory.preferences}")

    # 5. Verify Historical Pattern Storage and Semantic Retrieval
    semantic_search = SemanticSearch(memory_manager)

    logger.info("Testing semantic retrieval for similar goal...")
    query = "Summarize technical architecture"
    results = await semantic_search.find_relevant_patterns(query, user_id=user_id, limit=1)

    if results:
        logger.info(f"Successfully retrieved relevant pattern: {results[0].goal_request}")
        logger.info(f"Approach taken: {results[0].approach}")
        logger.info(f"Lessons extracted: {results[0].tags}")
    else:
        logger.warning("No relevant patterns found. Check if embeddings were generated and stored correctly.")

    logger.info("Memory System Verification Complete.")

if __name__ == "__main__":
    asyncio.run(verify_memory_system())
