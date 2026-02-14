from src.core.types import Plan, Step, TaskStatus

SAMPLE_STEP_1 = Step(
    step_id="step_001",
    action="web_search",
    description="Search for Python hello world examples",
    tools=["web_search"],
    dependencies=[],
    status=TaskStatus.PENDING,
    input_data={"query": "python hello world"},
    output_data={}
)

SAMPLE_STEP_2 = Step(
    step_id="step_002",
    action="document_generator",
    description="Write the code to a file",
    tools=["document_generator"],
    dependencies=["step_001"],
    status=TaskStatus.PENDING,
    input_data={"content": "print('hello world')"},
    output_data={}
)

SAMPLE_PLAN = Plan(
    task_id="task_test_001",
    steps=[SAMPLE_STEP_1, SAMPLE_STEP_2]
)
