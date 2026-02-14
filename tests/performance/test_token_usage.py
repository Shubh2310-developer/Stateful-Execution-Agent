import pytest
from src.llm.token_counter import token_counter

def test_token_counting_efficiency():
    """Tests the efficiency and accuracy of the token counter."""
    text = "This is a test sentence for token counting."
    count = token_counter.count_tokens(text)
    assert count > 0
    assert isinstance(count, int)

def test_prompt_template_token_load():
    """Verifies the token load of key system prompts to prevent context bloat."""
    from src.llm.prompt_builder import prompt_builder
    from src.core.types import Step

    # Test Planner Prompt Load
    planner_msgs = prompt_builder.build_planner_prompt(
        goal="Analyze global chip supply chain risks for 2025.",
        tool_list=["web_search", "web_scraper", "data_processor", "summarizer"],
        include_examples=True
    )
    planner_tokens = token_counter.count_message_tokens(planner_msgs)
    # Ensure it's substantial but not exceeding 4k tokens for base prompt
    assert 500 < planner_tokens < 4000

    # Test Executor Prompt Load
    step = Step(
        step_id="S1",
        action="web_search",
        description="Search for 2024 semiconductor foundry capacity reports.",
        tools=["web_search"]
    )
    executor_msgs = prompt_builder.build_executor_prompt(
        step=step,
        available_artifacts={"S0": "Target: Semiconductor industry"},
        tool_list=["web_search", "web_scraper"]
    )
    executor_tokens = token_counter.count_message_tokens(executor_msgs)
    assert 400 < executor_tokens < 3000

    # Test Reviewer Prompt Load
    reviewer_msgs = prompt_builder.build_reviewer_prompt(
        goal={"primary_objective": "Supply chain report"},
        plan_steps=[step.dict()],
        artifacts=[{"id": "art_1", "type": "document", "uri": "file://report.md"}]
    )
    reviewer_tokens = token_counter.count_message_tokens(reviewer_msgs)
    assert 300 < reviewer_tokens < 2500
