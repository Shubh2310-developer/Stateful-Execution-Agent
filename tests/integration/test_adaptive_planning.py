import pytest
import json
from datetime import datetime
from unittest.mock import AsyncMock, patch
from src.planner.planner import Planner
from src.core.types import UserMemory, Plan, Step
from src.llm.groq_client import groq_client

@pytest.mark.asyncio
async def test_adaptive_planning_integration():
    """
    Verifies that the Planner correctly utilizes the AdaptivePlanner
    to inject past experiences into the StepGenerator's prompt.
    """
    planner = Planner()
    user_id = "test_user_adaptive"

    # 1. Setup mock memory with a specific lesson
    user_memory = UserMemory(
        user_id=user_id,
        historical_patterns=[
            {
                "task_type": "data cleanup",
                "approach": "Always use the 'summarizer' after 'web_search'.",
                "feedback": "User preferred summarized results.",
                "timestamp": datetime.utcnow()
            }
        ],
        preferences={"format": "json"}
    )

    raw_goal = "Clean up some data from the web"
    available_tools = ["web_search", "summarizer"]

    # Mock LLM responses
    parsed_goal = {"primary_objective": "Clean up data"}

    # Capture messages to verify injection
    captured_messages = []

    async def mock_gen(messages):
        nonlocal captured_messages
        # StepGenerator is usually called when 'PAST EXPERIENCES' is likely in the prompt
        if any("PAST EXPERIENCES" in str(m.get("content")) for m in messages):
            captured_messages = messages
            return json.dumps({
                "reasoning": "Using past strategy",
                "steps": [{"step_id": "S1", "action": "web_search", "description": "search", "dependencies": []}]
            })

        # Goal Parser or Validator
        if "PRIMARY GOAL" in str(messages) and "PAST EXPERIENCES" not in str(messages):
            return json.dumps(parsed_goal)

        return json.dumps({"isValid": True, "feedback": "OK"})

    with patch.object(groq_client, "generate_response", side_effect=mock_gen):
        plan = await planner.create_plan(
            raw_goal=raw_goal,
            available_tools=available_tools,
            user_memory=user_memory
        )

    # 2. Assertions
    assert plan is not None
    assert len(captured_messages) > 0

    # Find the user message
    user_msg = next(m["content"] for m in captured_messages if m["role"] == "user")

    # Verify both blocks are present
    assert "PAST EXPERIENCES & LESSONS LEARNED" in user_msg
    assert "Always use the 'summarizer' after 'web_search'" in user_msg
    assert "USER PREFERENCES" in user_msg
