import sys
import os
import json
from datetime import datetime

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.llm.prompt_builder import PromptBuilder
from src.llm.response_parser import ResponseParser
from src.llm.token_counter import TokenCounter
from src.core.types import Step, TaskStatus, Plan, Goal
from pydantic import BaseModel

def test_prompt_builder():
    print("--- Testing PromptBuilder ---")
    builder = PromptBuilder()

    # 1. Test Planner Prompt
    goal = "Create a summary of AI news from today"
    tools = ["web_search", "web_scraper", "summarizer"]
    planner_messages = builder.build_planner_prompt(
        goal=goal,
        tool_list=tools,
        user_preferences={"style": "concise"},
        constraints=["Max 5 steps"]
    )
    print("\nPlanner User Prompt Sample:")
    print(planner_messages[1]["content"])

    # 2. Test Executor Prompt
    step = Step(
        id="step_001",
        action="web_search",
        description="Search for AI news",
        tools=["web_search"],
        input_data={"query": "AI news today"}
    )
    executor_messages = builder.build_executor_prompt(
        step=step,
        available_artifacts={},
        tool_list=tools
    )
    print("\nExecutor User Prompt Sample:")
    print(executor_messages[1]["content"])

    # 3. Test Replanning Prompt
    plan = Plan(steps=[step])
    replanning_messages = builder.build_replanning_prompt(
        goal=goal,
        plan=plan,
        feedback="The search returned no results.",
        available_artifacts={}
    )
    print("\nReplanning User Prompt Sample:")
    print(replanning_messages[1]["content"])

    # 4. Test Validator Prompt
    validator_messages = builder.build_validator_prompt(
        step_description="Search for AI news",
        success_criteria=["List of URLs found"],
        step_output={"urls": ["http://news.ai"]}
    )
    print("\nValidator User Prompt Sample:")
    print(validator_messages[1]["content"])

def test_response_parser():
    print("\n--- Testing ResponseParser ---")
    parser = ResponseParser()

    # 1. Test markdown JSON
    markdown_json = """
Here is the plan:
```json
{
  "action": "test_action",
  "parameters": {"key": "value"}
}
```
Hope this helps!
"""
    result = parser.parse_json_response(markdown_json)
    print(f"Parsed Markdown JSON: {result}")

    # 2. Test raw JSON with preamble
    raw_json_preamble = "The result is: {\"status\": \"success\"} because it worked."
    result = parser.parse_json_response(raw_json_preamble)
    print(f"Parsed Preamble JSON: {result}")

    # 3. Test JSON Repair (Trailing comma and single quotes)
    malformed_json = "{'status': 'success',}"
    result = parser.parse_json_response(malformed_json)
    print(f"Parsed & Repaired JSON: {result}")

    # 4. Test Pydantic validation
    class TestModel(BaseModel):
        name: str
        value: int

    valid_json = '{"name": "test", "value": 42}'
    result = parser.parse_json_response(valid_json, model_schema=TestModel)
    print(f"Parsed & Validated Pydantic: {result}")

def test_token_counter():
    print("\n--- Testing TokenCounter ---")
    counter = TokenCounter(model_name="llama3-70b-8192")
    text = "Hello world, this is a test of token counting."
    tokens = counter.count_tokens(text)
    cost = counter.calculate_cost(tokens, tokens)
    print(f"Tokens: {tokens}")
    print(f"Estimated Cost (Prompt+Completion): ${cost:.8f}")

if __name__ == "__main__":
    try:
        test_prompt_builder()
        test_response_parser()
        test_token_counter()
        print("\nAll verifications successful!")
    except Exception as e:
        print(f"\nVerification failed: {e}")
        import traceback
        traceback.print_exc()
