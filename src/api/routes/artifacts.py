from fastapi import APIRouter, HTTPException, Request
from src.state.state_manager import StateManager
from src.executor.artifact_manager import ArtifactManager
from typing import List, Dict, Any

router = APIRouter(prefix="/artifacts", tags=["artifacts"])
state_manager = StateManager()
artifact_manager = ArtifactManager()

@router.get("/task/{task_id}", response_model=List[Dict[str, Any]])
async def list_task_artifacts(request: Request, task_id: str):
    """Lists all artifacts associated with a task."""
    user = getattr(request.state, "user", None)
    current_user_id = user["id"] if user else None

    state = await state_manager.get_state(task_id)
    if not state:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

    # Session isolation
    if current_user_id and state.user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access these artifacts")

    return [art.dict() for art in state.artifacts]

@router.get("/{artifact_id}")
async def get_artifact_details(artifact_id: str):
    """Retrieves metadata for a specific artifact."""
    # In a full implementation, we'd have a separate artifact lookup
    # For now, we return a placeholder or search across active states
    raise HTTPException(status_code=501, detail="Direct artifact lookup by ID not yet implemented")
