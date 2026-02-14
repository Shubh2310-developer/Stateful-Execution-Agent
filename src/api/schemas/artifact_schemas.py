from typing import Any, Dict, List, Optional
from pydantic import BaseModel
from datetime import datetime

class ArtifactResponse(BaseModel):
    artifact_id: str
    task_id: str
    step_id: str
    type: str
    format: str
    storage_uri: str
    created_at: datetime

class ArtifactListResponse(BaseModel):
    artifacts: List[ArtifactResponse]
    total_count: int
