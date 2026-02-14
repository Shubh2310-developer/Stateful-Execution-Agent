import pytest
import json
from unittest.mock import AsyncMock, patch
from src.planner.planner import Planner
from src.core.types import Plan, Step
from src.llm.groq_client import groq_client

@pytest.mark.asyncio
async def test_planner_full_flow_success():
    planner = Planner()
    raw_goal = "Analyze revenue and generate a chart"
    available_tools = ["web_search", "chart_generator"]

    # 1. GoalParser response
    parsed_goal = {
        "primary_objective": "Analyze revenue and generate a chart",
        "constraints": [],
        "reasoning": "Parse goal"
    }

    # 2. StepGenerator response
    llm_plan_json = {
        "reasoning": "Plan strategy",
        "steps": [
            {
                "step_id": "S1",
                "action": "web_search",
                "description": "Search for revenue data",
                "dependencies": [],
                "success_criteria": "Data found"
            },
            {
                "step_id": "S2",
                "action": "web_search",
                "description": "Extract specific figures",
                "dependencies": ["S1"],
                "success_criteria": "Figures extracted"
            },
            {
                "step_id": "S3",
                "action": "chart_generator",
                "description": "Generate revenue chart",
                "dependencies": ["S2"],
                "success_criteria": "Chart generated"
            }
        ]
    }

    # 3. PlanValidator response
    validator_response = {
        "isValid": True,
        "feedback": "Perfect plan"
    }

    # Patch the global instance method
    with patch.object(groq_client, "generate_response", new_callable=AsyncMock) as mock_gen:
        mock_gen.side_effect = [
            json.dumps(parsed_goal),
            json.dumps(llm_plan_json),
            json.dumps(validator_response)
        ]

        plan = await planner.create_plan(raw_goal, available_tools)

        assert len(plan.steps) == 3
        assert plan.steps[0].step_id == "S1"
        assert plan.steps[2].step_id == "S3"
        assert plan.steps[2].action == "chart_generator"
        assert "chart_generator" in plan.steps[2].tools
        assert mock_gen.call_count == 3

@pytest.mark.asyncio
async def test_planner_retry_on_validation_failure():
    planner = Planner()
    raw_goal = "Test goal"
    available_tools = ["tool1"]

    parsed_goal = {"primary_objective": "Test goal"}

    # Attempt 1: fails
    fail_plan = {"reasoning": "fail", "steps": [{"step_id": "S1", "action": "tool1", "description": "d1", "dependencies": []}]}
    fail_val = {"isValid": False, "feedback": "Missing detail"}

    # Attempt 2: succeeds
    success_plan = {"reasoning": "success", "steps": [{"step_id": "S1", "action": "tool1", "description": "d1", "dependencies": []}]}
    success_val = {"isValid": True, "feedback": "Fixed"}

    with patch.object(groq_client, "generate_response", new_callable=AsyncMock) as mock_gen:
        mock_gen.side_effect = [
            json.dumps(parsed_goal),
            json.dumps(fail_plan),
            json.dumps(fail_val),
            json.dumps(success_plan),
            json.dumps(success_val)
        ]

        plan = await planner.create_plan(raw_goal, available_tools)

        assert plan is not None
        assert len(plan.steps) == 1
        assert mock_gen.call_count == 5
