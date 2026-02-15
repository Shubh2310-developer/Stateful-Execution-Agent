import asyncio
import json
from datetime import datetime, timezone
from typing import List, Dict, Any

from src.planner.planner import Planner
from src.core.types import UserMemory, Goal, TaskStatus
from src.llm.groq_client import groq_client
from unittest.mock import AsyncMock, patch

async def demo_adaptive_planning():
    print("=== Adaptive Planning Integration Demo ===")

    # 1. Setup Mock User Memory with past experiences
    # This represents 'Lessons Learned' from Phase 4.5
    user_memory = UserMemory(
        user_id="user_123",
        preferences={"format": "detailed_markdown"},
        historical_patterns=[
            {
                "task_type": "revenue analysis",
                "approach": "Used web_search to find competitor data first, then used data_processor.",
                "feedback": "The user liked the competitor comparison.",
                "timestamp": datetime.now(timezone.utc)
            },
            {
                "task_type": "market research",
                "approach": "Summarized findings using the summarizer tool before final report.",
                "feedback": "Effective for long documents.",
                "timestamp": datetime.now(timezone.utc)
            }
        ]
    )

    planner = Planner()
    raw_goal = "Analyze revenue for Q4 and compare with competitors"
    available_tools = ["web_search", "data_processor", "summarizer"]

    print(f"\nGoal: {raw_goal}")
    print(f"Memory contains {len(user_memory.historical_patterns)} past experiences.")

    # 2. Mock LLM responses to see the flow without actual API calls
    # We want to verify that the 'past_experiences' actually reach the prompt

    parsed_goal = {
        "primary_objective": "Analyze Q4 revenue and competitor comparison",
        "constraints": ["Use recent data"],
        "reasoning": "Needs web search and data processing."
    }

    mock_plan = {
        "reasoning": "Based on past successful revenue analysis, I will prioritize competitor search.",
        "steps": [
            {
                "step_id": "S1",
                "action": "web_search",
                "description": "Search for Q4 revenue and competitor performance",
                "dependencies": [],
                "success_criteria": "Data collected"
            },
            {
                "step_id": "S2",
                "action": "data_processor",
                "description": "Compare internal revenue with competitor data",
                "dependencies": ["S1"],
                "success_criteria": "Comparison complete"
            }
        ]
    }

    validator_response = {"isValid": True, "feedback": "Looks good"}

    # We'll use a wrapper to capture the prompt sent to the LLM
    captured_messages = []

    async def mocked_generate(messages):
        nonlocal captured_messages
        # We only care about the StepGenerator call (usually the 2nd call in Planner)
        if any("PAST EXPERIENCES" in str(m.get("content")) for m in messages):
            captured_messages = messages

        # Return appropriate mock based on call count or content
        content = str(messages)
        if "PRIMARY GOAL" in content and "PAST EXPERIENCES" not in content:
            return json.dumps(parsed_goal)
        elif "PAST EXPERIENCES" in content:
            return json.dumps(mock_plan)
        else:
            return json.dumps(validator_response)

    print("\nExecuting Planner.create_plan()...")
    with patch.object(groq_client, "generate_response", side_effect=mocked_generate):
        plan = await planner.create_plan(
            raw_goal=raw_goal,
            available_tools=available_tools,
            user_memory=user_memory
        )

    # 3. Verify that the prompt included the relevant memory
    print("\n=== Verification ===")
    if captured_messages:
        user_message = next(m for m in captured_messages if m["role"] == "user")
        content = user_message["content"]

        print("Searching for 'PAST EXPERIENCES' in the generated prompt...")
        if "PAST EXPERIENCES & LESSONS LEARNED" in content:
            print("SUCCESS: Past experiences block found in prompt!")

            # Check if the specific relevant lesson was injected
            if "revenue analysis" in content:
                print("SUCCESS: Relevant lesson 'revenue analysis' was injected.")
            else:
                print("FAILURE: Relevant lesson not found.")
        else:
            print("FAILURE: Past experiences block missing from prompt.")
    else:
        print("FAILURE: Could not capture StepGenerator prompt.")

    print("\nGenerated Plan Reasoning:")
    print(f"'{plan.metadata.get('reasoning', 'N/A')}'" if hasattr(plan, 'metadata') else "Check reasoning in logs")

    for step in plan.steps:
        print(f"- [{step.step_id}] {step.action}: {step.description}")

if __name__ == "__main__":
    asyncio.run(demo_adaptive_planning())
