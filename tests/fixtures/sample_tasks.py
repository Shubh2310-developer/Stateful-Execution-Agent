from datetime import datetime, timezone

SAMPLE_TASK_DATA = {
    "task_id": "task_test_001",
    "user_id": "usr_test_123",
    "version_counter": 1,
    "goal": {
        "request": "Write a hello world script in Python",
        "primary_objective": "Create a Python script that prints 'Hello, World!'",
        "success_criteria": ["Script exists", "Script runs", "Output is correct"]
    },
    "status": "pending",
    "created_at": datetime.now(timezone.utc),
    "updated_at": datetime.now(timezone.utc)
}

SAMPLE_TASK_LIST = [
    SAMPLE_TASK_DATA,
    {
        "task_id": "task_test_002",
        "user_id": "usr_test_123",
        "version_counter": 1,
        "goal": {"request": "Research climate change"},
        "status": "completed",
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc)
    }
]
