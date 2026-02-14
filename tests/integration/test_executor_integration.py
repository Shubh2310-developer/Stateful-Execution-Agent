import pytest
import json
from unittest.mock import AsyncMock, patch, MagicMock
from src.executor.executor import Executor
from src.core.types import TaskState, Plan, Step, Artifact, Goal, TaskStatus
from src.llm.groq_client import groq_client

@pytest.mark.asyncio
async def test_executor_full_flow_success():
    executor = Executor()

    # 1. Setup Task State with a 2-step plan
    step1 = Step(
        step_id="S1", action="web_search",
        description="Search for info", success_criteria="Info found"
    )
    step2 = Step(
        step_id="S2", action="summarizer",
        description="Summarize info", dependencies=["S1"],
        success_criteria="Summary created"
    )

    state = TaskState(
        task_id="task_exec_1",
        user_id="user_1",
        status=TaskStatus.PENDING,
        goal=Goal(request="Summarize news", success_criteria=["News summarized"]),
        plan=Plan(task_id="task_exec_1", steps=[step1, step2])
    )

    # 2. Mock Tool Outputs
    search_result = {"results": "Simulated news content"}
    summary_result = "This is a summary of simulated news."

    # 3. Mock LLM Decisions and Validations
    # Step 1 Decision, Step 1 Validation, Step 2 Decision, Step 2 Validation
    decisions_and_vals = [
        # S1 Decision
        json.dumps({
            "action": "web_search",
            "parameters": {"query": "latest news"},
            "reasoning": "Need to find news",
            "confidence": 0.9
        }),
        # S1 Validation
        json.dumps({
            "passed": True,
            "reasoning": "Data looks good",
            "quality_score": 0.8
        }),
        # S2 Decision
        json.dumps({
            "action": "summarizer",
            "parameters": {"text": str(search_result)},
            "reasoning": "Now summarizing",
            "confidence": 0.95
        }),
        # S2 Validation
        json.dumps({
            "passed": True,
            "reasoning": "Summary is perfect",
            "quality_score": 0.9
        })
    ]

    # Patch Groq and Tool Orchestrator
    with patch.object(groq_client, "generate_response", new_callable=AsyncMock) as mock_gen, \
         patch.object(executor.step_runner.tool_orchestrator, "invoke_tool", new_callable=AsyncMock) as mock_invoke:

        mock_gen.side_effect = decisions_and_vals
        mock_invoke.side_effect = [search_result, summary_result]

        # 4. Run execution
        updated_state = await executor.execute_plan(state)

        # 5. Verify results
        assert updated_state.status == TaskStatus.COMPLETED
        assert len(updated_state.artifacts) == 2
        assert len(updated_state.decisions) == 2
        assert updated_state.current_step_index == 2

        assert updated_state.plan.steps[0].status == TaskStatus.COMPLETED
        assert updated_state.plan.steps[1].status == TaskStatus.COMPLETED

        assert mock_gen.call_count == 4
        assert mock_invoke.call_count == 2
