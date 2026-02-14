from src.core.types import Plan, Step

SAMPLE_STEP_1 = Step(
    step_id="step_001",
    order=1,
    action="web_search",
    description="Search for Python hello world examples",
    success_criteria="Found at least one example",
    tools_needed=["web_search"]
)

SAMPLE_STEP_2 = Step(
    step_id="step_002",
    order=2,
    action="document_generator",
    description="Write the code to a file",
    success_criteria="File 'hello.py' created with correct content",
    dependencies=["step_001"],
    tools_needed=["document_generator"]
)

SAMPLE_PLAN = Plan(
    task_id="task_test_001",
    goal_summary="Create a hello world python script",
    steps=[SAMPLE_STEP_1, SAMPLE_STEP_2],
    total_estimated_duration_minutes=5,
    risk_assessment="low"
)
