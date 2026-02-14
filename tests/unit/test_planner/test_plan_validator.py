import pytest
from src.planner.plan_validator import PlanValidator
from src.core.types import Plan, Step
from src.core.exceptions import ValidationError
from tests.fixtures.sample_plans import SAMPLE_PLAN

def test_plan_validator_success():
    validator = PlanValidator()
    # SAMPLE_PLAN has tools: web_search, document_generator
    available_tools = ["web_search", "document_generator"]

    assert validator.validate(SAMPLE_PLAN, available_tools) is True

def test_plan_validator_no_steps():
    validator = PlanValidator()
    empty_plan = Plan(task_id="test", goal_summary="test", steps=[])

    with pytest.raises(ValidationError, match="Plan contains no steps"):
        validator.validate(empty_plan, [])

def test_plan_validator_missing_dependency():
    validator = PlanValidator()
    step = Step(
        step_id="step_2", order=2, action="act",
        description="desc", success_criteria="done",
        dependencies=["non_existent"]
    )
    invalid_plan = Plan(task_id="test", goal_summary="test", steps=[step])

    with pytest.raises(ValidationError, match="depends on non-existent step: non_existent"):
        validator.validate(invalid_plan, ["act"])
