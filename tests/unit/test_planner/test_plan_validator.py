import pytest
from unittest.mock import AsyncMock, patch
from src.planner.plan_validator import PlanValidator
from src.core.types import Plan, Step
from tests.fixtures.sample_plans import SAMPLE_PLAN

@pytest.mark.asyncio
async def test_plan_validator_success():
    validator = PlanValidator()
    # SAMPLE_PLAN has tools: web_search, document_generator
    available_tools = ["web_search", "document_generator"]
    goal = {"primary_objective": "test goal"}

    # Mock LLM response for semantic validation
    with patch("src.planner.plan_validator.groq_client") as mock_groq:
        mock_groq.generate_response = AsyncMock(return_value='{"isValid": true, "feedback": "Looks good", "risks": []}')

        result = await validator.validate(SAMPLE_PLAN, goal, available_tools)
        assert result["isValid"] is True

@pytest.mark.asyncio
async def test_plan_validator_no_steps():
    validator = PlanValidator()
    empty_plan = Plan(task_id="test", steps=[])

    result = await validator.validate(empty_plan, {}, [])
    assert result["isValid"] is False
    assert "no steps" in result["feedback"]

@pytest.mark.asyncio
async def test_plan_validator_duplicate_ids():
    validator = PlanValidator()
    step = Step(step_id="s1", action="a", description="d")
    plan = Plan(task_id="test", steps=[step, step])

    result = await validator.validate(plan, {}, ["a"])
    assert result["isValid"] is False
    assert "duplicate step IDs" in result["feedback"]
