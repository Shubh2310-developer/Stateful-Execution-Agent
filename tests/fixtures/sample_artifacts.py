from datetime import datetime
from src.core.types import Artifact

SAMPLE_ARTIFACT_1 = Artifact(
    id="art_test_001",
    task_id="task_test_001",
    step_id="step_001",
    uri="file:///tmp/test_art_1.json",
    type="data",
    checksum="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    size_bytes=1024,
    mime_type="application/json",
    metadata={"source": "test_fixture", "format": "json"},
    created_at=datetime.utcnow()
)

SAMPLE_ARTIFACT_2 = Artifact(
    id="art_test_002",
    task_id="task_test_001",
    step_id="step_002",
    uri="file:///tmp/hello.py",
    type="code",
    checksum="f6015707759f239276d1e4313d4b68427f6776b92f37c37617d3b0c3716d934e",
    size_bytes=42,
    mime_type="text/x-python",
    metadata={"lang": "python", "format": "txt"},
    created_at=datetime.utcnow()
)
