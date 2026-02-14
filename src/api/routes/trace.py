from fastapi import APIRouter, HTTPException
from src.state.state_manager import StateManager
from typing import List, Dict, Any

router = APIRouter(prefix="/trace", tags=["trace"])
state_manager = StateManager()

@router.get("/{task_id}")
async def get_task_trace(task_id: str):
    """Retrieves the decision trace for a specific task."""
    state = await state_manager.get_state(task_id)
    if not state:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

    return {
        "task_id": task_id,
        "decisions": [d.dict() for d in state.decisions]
    }
