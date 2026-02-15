import asyncio
import json
from datetime import datetime, timezone
from typing import List, Dict, Any
from unittest.mock import AsyncMock, patch

from src.core.types import TaskState, Goal, TaskStatus, StepLog, Artifact, UserMemory, UserProfile, UserPreferences
from src.memory.learning.adaptation_engine import AdaptationEngine
from src.llm.groq_client import groq_client

async def demo_learning_loop():
    print("=== Learning Loop (Reflection) Demo ===")

    # 1. Setup a completed Task State with logs and artifacts
    state = TaskState(
        task_id="task_demo_789",
        user_id="user_123",
        status=TaskStatus.COMPLETED,
        goal=Goal(
            request="Create a summary of the latest AI news and format it as a table.",
            success_criteria=["Summary produced", "Table format used"]
        ),
        logs=[
            StepLog(
                step_id="S1",
                action="web_search",
                description="Search for latest AI news",
                output="Found news about Gemini 1.5, Claude 3, and GPT-4o."
            ),
            StepLog(
                step_id="S2",
                action="summarizer",
                description="Summarize the news",
                output="AI models are getting faster and more multimodal."
            ),
            StepLog(
                step_id="S3",
                action="document_generator",
                description="Format as table",
                output="| Model | Feature |\n|---|---|\n| Gemini | 1M context |"
            )
        ],
        artifacts=[
            Artifact(id="art_1", task_id="task_demo_789", type="document", uri="ai_news_summary.md")
        ],
        updated_at=datetime.now(timezone.utc)
    )

    feedback = {"content": "Great summary, but I prefer more technical details in the future.", "rating": 4}

    # 2. Mock LLM Reflection Response
    mock_reflection = {
        "reasoning": "The agent followed the steps correctly. User feedback indicates a preference for 'technical details', which was not explicitly captured in the initial constraints but should be a learned preference.",
        "insights": ["User values technical depth over high-level summaries."],
        "corrections": ["In future news tasks, look for architecture and parameter details."],
        "patterns": {
            "task_category": "news_summarization",
            "successful_approach": "Sequenced web_search -> summarizer -> formatter.",
            "confidence_score": 0.9
        },
        "user_preference_updates": {
            "technical_depth": "high",
            "detail_level": "high"
        }
    }

    # 3. Setup Adaptation Engine with mocked components
    with patch("src.memory.learning.adaptation_engine.groq_client.generate_response", new_callable=AsyncMock) as mock_gen, \
         patch("src.memory.learning.adaptation_engine.MemoryManager") as mock_mm_class:

        mock_mm = mock_mm_class.return_value
        mock_mm.update_user_preferences = AsyncMock()
        mock_mm.add_historical_pattern = AsyncMock()

        mock_gen.return_value = json.dumps(mock_reflection)

        engine = AdaptationEngine(memory_manager=mock_mm)

        print(f"\nTask Goal: {state.goal.request}")
        print(f"Status: {state.status.value}")
        print(f"Feedback: {feedback['content']}")

        print("\nRunning Learning Loop (Reflection)...")
        reflection = await engine.learn_from_task(state, feedback)

        # 4. Show Results
        print("\n=== Reflection Results ===")
        print(f"Reasoning: {reflection.get('reasoning')}")
        print(f"Insights: {reflection.get('insights')}")
        print(f"Patterns: {reflection.get('patterns', {}).get('successful_approach')}")
        print(f"Learned Preference Updates: {reflection.get('user_preference_updates')}")

        # Verify Mocks
        if mock_mm.update_user_preferences.called:
            print("\nSUCCESS: User preferences were updated in Long-Term Memory.")
        if mock_mm.add_historical_pattern.called:
            print("SUCCESS: Historical pattern was stored for future retrieval.")

if __name__ == "__main__":
    asyncio.run(demo_learning_loop())
