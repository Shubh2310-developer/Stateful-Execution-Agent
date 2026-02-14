import sys
import os
import json
from typing import Any, Dict, List

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.llm.prompt_builder import PromptBuilder
from src.core.types import Step, TaskStatus, Plan, Goal, Artifact
from pydantic import BaseModel

def verify_cot_prompts():
    print("=== Production Prompt Validation Harness ===")
    builder = PromptBuilder()

    # 1. Goal Parser
    print("\n--- [GOAL PARSER] ---")
    goal_messages = builder.build_goal_parser_prompt(
        raw_goal="Calculate the carbon footprint of a flight from NYC to London.",
        context={"user_id": "user_123"}
    )
    print(f"System Prompt Length: {len(goal_messages[0]['content'])}")
    print(f"User Prompt Sample: {goal_messages[1]['content'][:200]}...")

    # 2. Planner
    print("\n--- [PLANNER] ---")
    planner_messages = builder.build_planner_prompt(
        goal="Analyze quarterly revenue trends for Nvidia.",
        tool_list=["web_search", "web_scraper", "data_processor", "chart_generator"],
        lessons_learned=["User prefers line charts for financial data."]
    )
    print(f"System Prompt Length: {len(planner_messages[0]['content'])}")
    print(f"User Prompt Sample: {planner_messages[1]['content'][:200]}...")

    # 3. Executor
    print("\n--- [EXECUTOR] ---")
    step = Step(
        step_id="S1",
        action="web_search",
        description="Search for Nvidia Q3 2024 revenue results.",
        tools=["web_search"]
    )
    executor_messages = builder.build_executor_prompt(
        step=step,
        available_artifacts={"S0_context": "Financial analysis target: Nvidia"},
        tool_list=["web_search", "web_scraper"]
    )
    print(f"System Prompt Length: {len(executor_messages[0]['content'])}")
    print(f"User Prompt Sample: {executor_messages[1]['content'][:200]}...")

    # 4. Plan Validator
    print("\n--- [PLAN VALIDATOR] ---")
    plan_steps = [
        {"step_id": "S1", "action": "web_search", "description": "Search data", "dependencies": [], "success_criteria": "Data found"}
    ]
    validator_messages = builder.build_plan_validator_prompt(
        goal={"primary_objective": "Search data"},
        steps=plan_steps,
        available_tools=["web_search"]
    )
    print(f"System Prompt Length: {len(validator_messages[0]['content'])}")
    print(f"User Prompt Sample: {validator_messages[1]['content'][:200]}...")

    # 5. Reviewer
    print("\n--- [REVIEWER] ---")
    reviewer_messages = builder.build_reviewer_prompt(
        goal={"primary_objective": "Final report"},
        plan_steps=plan_steps,
        artifacts=[{"id": "art_1", "type": "document", "uri": "file://report.md"}]
    )
    print(f"System Prompt Length: {len(reviewer_messages[0]['content'])}")
    print(f"User Prompt Sample: {reviewer_messages[1]['content'][:200]}...")

    # 6. Quality Checker
    print("\n--- [QUALITY CHECKER] ---")
    qc_messages = builder.build_quality_checker_prompt(
        artifact_type="document",
        artifact_id="art_1",
        content="This is the final report on Nvidia revenue."
    )
    print(f"System Prompt Length: {len(qc_messages[0]['content'])}")
    print(f"User Prompt Sample: {qc_messages[1]['content'][:200]}...")

    # 7. Summarizer Tool
    print("\n--- [SUMMARIZER TOOL] ---")
    summarizer_messages = builder.build_summarizer_prompt(
        text="Long text about Nvidia and AI chips...",
        focus="Revenue details"
    )
    print(f"System Prompt Length: {len(summarizer_messages[0]['content'])}")
    print(f"User Prompt Sample: {summarizer_messages[1]['content'][:200]}...")

if __name__ == "__main__":
    try:
        verify_cot_prompts()
        print("\nAll templates rendered successfully!")
    except Exception as e:
        print(f"\nVerification failed: {e}")
        import traceback
        traceback.print_exc()
