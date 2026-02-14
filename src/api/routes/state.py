from fastapi import APIRouter, HTTPException
from src.state.state_manager import StateManager
from src.utils.logger import logger

router = APIRouter(prefix="/state", tags=["state"])
state_manager = StateManager()

@router.get("/{task_id}")
async def get_task_state(task_id: str):
    """Retrieves the full state of a task."""
    state = await state_manager.get_state(task_id)
    if not state:
        raise HTTPException(status_code=404, detail=f"State for task {task_id} not found")
    return state.dict()
