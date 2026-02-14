from datetime import datetime
from src.core.types import Artifact

SAMPLE_ARTIFACT_1 = Artifact(
    artifact_id="art_test_001",
    task_id="task_test_001",
    step_id="step_001",
    type="data",
    format="json",
    storage_uri="file:///tmp/test_art_1.json",
    content_preview='{"results": ["https://python.org"]}',
    metadata={"source": "test_fixture"},
    created_at=datetime.utcnow()
)

SAMPLE_ARTIFACT_2 = Artifact(
    artifact_id="art_test_002",
    task_id="task_test_001",
    step_id="step_002",
    type="code",
    format="txt",
    storage_uri="file:///tmp/hello.py",
    content_preview="print('Hello, World!')",
    metadata={"lang": "python"},
    created_at=datetime.utcnow()
)
