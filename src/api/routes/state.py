from fastapi import APIRouter, HTTPException, Request
from src.state.state_manager import StateManager
from src.utils.logger import logger

router = APIRouter(prefix="/state", tags=["state"])
state_manager = StateManager()

@router.get("/{task_id}")
async def get_task_state(request: Request, task_id: str):
    """Retrieves the full state of a task."""
    user = getattr(request.state, "user", None)
    current_user_id = user["id"] if user else None

    state = await state_manager.get_state(task_id)
    if not state:
        raise HTTPException(status_code=404, detail=f"State for task {task_id} not found")

    # Session isolation
    if current_user_id and state.user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this state")

    return state.dict()
