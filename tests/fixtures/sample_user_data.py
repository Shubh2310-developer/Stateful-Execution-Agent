from datetime import datetime
from src.core.types import UserMemory

SAMPLE_USER_MEMORY = UserMemory(
    user_id="usr_test_123",
    profile={
        "user_id": "usr_test_123",
        "role": "QA Engineer",
        "company": "TestCorp",
        "industry": "Software"
    },
    preferences={
        "document_tone": "concise",
        "detail_level": "low"
    },
    domain_knowledge={
        "preferred_language": "Python"
    },
    historical_patterns=[
        {
            "task_type": "coding",
            "approach": "direct implementation",
            "success_score": 0.95
        }
    ],
    last_updated=datetime.utcnow()
)
