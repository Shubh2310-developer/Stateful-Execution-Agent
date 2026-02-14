from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any, Optional
from src.api.schemas.task_schemas import TaskCreate, TaskUpdate, TaskResponse
from src.orchestration.task_router import TaskRouter
from src.utils.logger import logger

router = APIRouter(prefix="/tasks", tags=["tasks"])
task_router = TaskRouter()

@router.post("/create", response_model=Dict[str, Any])
async def create_task(request: TaskCreate):
    """Initializes a new task and generates an execution plan."""
    logger.info(f"Received task creation request for user: {request.user_id}")
    try:
        result = await task_router.handle_request(
            user_id=request.user_id,
            goal=request.goal
        )
        return result
    except Exception as e:
        logger.exception("Failed to create task")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{task_id}/status")
async def get_task_status(task_id: str):
    """Retrieves the current status and progress of a task."""
    logger.info(f"Fetching status for task: {task_id}")
    try:
        state = await task_router.session_manager.get_session(task_id)
        if not state:
            raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

        # Calculate progress
        total_steps = len(state.plan.steps) if state.plan else 0
        progress_pct = (state.current_step_index / total_steps * 100) if total_steps > 0 else 0

        return {
            "task_id": task_id,
            "status": state.status,
            "progress": {
                "completed_steps": state.current_step_index,
                "total_steps": total_steps,
                "percentage": progress_pct,
                "current_step": state.plan.steps[state.current_step_index].step_id if state.plan and state.current_step_index < total_steps else None
            },
            "artifacts_produced": len(state.artifacts),
            "last_activity": state.updated_at.isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error fetching status for task {task_id}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{task_id}/continue")
async def continue_task(task_id: str, request: TaskUpdate):
    """Resumes or modifies a paused or failed task."""
    logger.info(f"Received continuation request for task: {task_id}")
    try:
        # In a real impl, we'd look up the user_id from the session
        # For simplicity, we assume we can resume without explicit user_id here
        state = await task_router.session_manager.get_session(task_id)
        if not state:
            raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

        result = await task_router.handle_request(
            user_id=state.user_id,
            goal=request.user_input or state.goal.get("request", ""),
            task_id=task_id
        )
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Failed to continue task {task_id}")
        raise HTTPException(status_code=500, detail=str(e))
