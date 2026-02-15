from fastapi import APIRouter, HTTPException, Depends, Request, BackgroundTasks
from typing import List, Dict, Any, Optional
from src.api.schemas.task_schemas import (
    TaskCreate, TaskUpdate, TaskResponse, TaskStatusResponse,
    FeedbackSubmission, FeedbackResponse, PreferenceUpdateResponse, FeedbackInsightResponse
)
from src.orchestration.task_router import TaskRouter
from src.core.types import TaskStatus
from src.memory.learning.feedback_processor import FeedbackProcessor
from src.state.persistence.database_adapter import DatabaseAdapter
from src.utils.logger import logger

router = APIRouter(prefix="/tasks", tags=["tasks"])
task_router = TaskRouter()
db_adapter = DatabaseAdapter()
feedback_processor = FeedbackProcessor(db_adapter=db_adapter)

@router.get("", response_model=list)
async def list_tasks(request: Request, limit: int = 50, skip: int = 0):
    """List all tasks with pagination."""
    # Use the tasks collection from db_adapter
    cursor = db_adapter.tasks.find({}, {
        "task_id": 1,
        "status": 1,
        "goal": 1,
        "created_at": 1,
        "updated_at": 1,
        "plan": 1,
        "artifacts": 1,
        "progress": 1,
        "_id": 0
    }).sort("created_at", -1).skip(skip).limit(limit)
    
    tasks = await cursor.to_list(length=limit)
    
    # Format for frontend
    formatted_tasks = []
    for task in tasks:
        formatted_tasks.append({
            "task_id": task.get("task_id"),
            "status": task.get("status"),
            "goal": task.get("goal", {}).get("request", ""),
            "created_at": task.get("created_at").isoformat() if task.get("created_at") else None,
            "updated_at": task.get("updated_at").isoformat() if task.get("updated_at") else None,
            "plan": task.get("plan"),
            "artifacts_produced": len(task.get("artifacts", [])),
            "progress": task.get("progress", 0)
        })
    
    return formatted_tasks


@router.post("", response_model=TaskResponse, status_code=201)
async def create_task(request: Request, task_data: TaskCreate, background_tasks: BackgroundTasks):
    """Initializes a new task and starts background execution."""
    user = getattr(request.state, "user", None)
    user_id = user["id"] if user else task_data.user_id

    logger.info(f"Received task creation request for user: {user_id}")
    try:
        state = await task_router.initialize_task(
            user_id=user_id,
            goal=task_data.goal
        )

        # Start execution in background
        background_tasks.add_task(task_router.run_task_cycle, state.task_id)

        return TaskResponse(
            task_id=state.task_id,
            status=state.status,
            goal_summary=state.goal.request[:100],
            progress_percentage=0.0,
            message="Task initialized and execution started in background"
        )
    except Exception as e:
        logger.exception("Failed to create task")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{task_id}", response_model=TaskStatusResponse)
async def get_task_status(request: Request, task_id: str):
    """Retrieves the current status and progress of a task."""
    user = getattr(request.state, "user", None)
    current_user_id = user["id"] if user else None

    logger.info(f"Fetching status for task: {task_id}")
    try:
        state = await task_router.session_manager.get_session(task_id)
        if not state:
            raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

        # Session isolation: Ensure user only sees their own tasks
        if current_user_id and state.user_id != current_user_id:
            logger.warning(f"User {current_user_id} attempted to access task {task_id} belonging to {state.user_id}")
            raise HTTPException(status_code=403, detail="Not authorized to access this task")

        # Calculate progress
        total_steps = len(state.plan.steps) if state.plan else 0
        progress_pct = (state.current_step_index / total_steps * 100) if total_steps > 0 else 0

        current_step_id = None
        if state.plan and state.current_step_index < len(state.plan.steps):
            current_step_id = state.plan.steps[state.current_step_index].step_id

        return TaskStatusResponse(
            task_id=task_id,
            status=state.status,
            progress={
                "completed_steps": state.current_step_index,
                "total_steps": total_steps,
                "percentage": progress_pct,
                "current_step": current_step_id
            },
            artifacts_produced=len(state.artifacts),
            last_activity=state.updated_at.isoformat()
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error fetching status for task {task_id}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{task_id}/continue", response_model=TaskResponse)
async def continue_task(request: Request, task_id: str, update_data: TaskUpdate, background_tasks: BackgroundTasks):
    """Resumes or modifies a paused or failed task."""
    user = getattr(request.state, "user", None)
    current_user_id = user["id"] if user else None

    logger.info(f"Received continuation request for task: {task_id}")
    try:
        state = await task_router.session_manager.get_session(task_id)
        if not state:
            raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

        # Session isolation: Ensure user only modifies their own tasks
        if current_user_id and state.user_id != current_user_id:
            logger.warning(f"User {current_user_id} attempted to modify task {task_id} belonging to {state.user_id}")
            raise HTTPException(status_code=403, detail="Not authorized to modify this task")

        updated_state = await task_router.handle_continuation(
            task_id=task_id,
            user_input=update_data.user_input,
            mode=update_data.mode
        )

        # Resume background execution
        background_tasks.add_task(task_router.run_task_cycle, task_id)

        total_steps = len(updated_state.plan.steps) if updated_state.plan else 0
        progress_pct = (updated_state.current_step_index / total_steps * 100) if total_steps > 0 else 0

        return TaskResponse(
            task_id=task_id,
            status=updated_state.status,
            goal_summary=updated_state.goal.request[:100],
            progress_percentage=progress_pct,
            message=f"Task resumed with mode: {update_data.mode}"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Failed to continue task {task_id}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{task_id}/pause", response_model=TaskResponse)
async def pause_task(request: Request, task_id: str):
    """Pauses a currently running task."""
    user = getattr(request.state, "user", None)
    current_user_id = user["id"] if user else None

    logger.info(f"Received pause request for task: {task_id}")
    try:
        state = await task_router.session_manager.get_session(task_id)
        if not state:
            raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

        if current_user_id and state.user_id != current_user_id:
            raise HTTPException(status_code=403, detail="Not authorized to modify this task")

        state.status = TaskStatus.PAUSED
        await task_router.session_manager.state_manager.save_state(state)

        total_steps = len(state.plan.steps) if state.plan else 0
        progress_pct = (state.current_step_index / total_steps * 100) if total_steps > 0 else 0

        return TaskResponse(
            task_id=task_id,
            status=state.status,
            goal_summary=state.goal.request[:100],
            progress_percentage=progress_pct,
            message="Task paused successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Failed to pause task {task_id}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{task_id}/feedback", response_model=FeedbackResponse, status_code=201)
async def submit_feedback(request: Request, task_id: str, feedback: FeedbackSubmission):
    """
    Submit user feedback for a completed task.

    This endpoint processes user feedback and updates:
    - User preferences based on feedback content
    - Historical patterns for future reference
    - Actionable insights for system improvement

    Args:
        task_id: The task identifier
        feedback: FeedbackSubmission with rating (1-5) and optional text

    Returns:
        FeedbackResponse with processing results, insights, and recommendations
    """
    user = getattr(request.state, "user", None)
    current_user_id = user["id"] if user else None

    logger.info(f"Received feedback for task: {task_id}, rating: {feedback.rating}/5")

    try:
        # Verify task exists
        state = await task_router.session_manager.get_session(task_id)
        if not state:
            raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

        # Session isolation: Ensure user only provides feedback for their own tasks
        if current_user_id and state.user_id != current_user_id:
            logger.warning(f"User {current_user_id} attempted to provide feedback for task {task_id} belonging to {state.user_id}")
            raise HTTPException(status_code=403, detail="Not authorized to provide feedback for this task")

        # Use the task's user_id for feedback processing
        user_id = state.user_id

        # Process feedback through FeedbackProcessor
        result = await feedback_processor.process_feedback(
            task_id=task_id,
            user_id=user_id,
            rating=feedback.rating,
            text_feedback=feedback.text_feedback
        )

        # Check for errors in processing
        if "error" in result:
            logger.error(f"Feedback processing failed: {result['error']}")
            raise HTTPException(status_code=500, detail=f"Feedback processing failed: {result['error']}")

        # Convert result to response schema
        preference_updates = [
            PreferenceUpdateResponse(**update) for update in result.get("preference_updates", [])
        ]

        insights = [
            FeedbackInsightResponse(**insight) for insight in result.get("insights", [])
        ]

        response = FeedbackResponse(
            feedback_id=result["feedback_id"],
            processed_at=result["processed_at"],
            sentiment=result["sentiment"],
            categories=result["categories"],
            correlations=result.get("correlations", {}),
            preference_updates=preference_updates,
            historical_pattern_updated=result.get("historical_pattern_updated", False),
            insights=insights,
            recommendations_for_future=result.get("recommendations_for_future", [])
        )

        logger.info(f"Successfully processed feedback {result['feedback_id']} for task {task_id}")
        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Failed to submit feedback for task {task_id}")
        raise HTTPException(status_code=500, detail=str(e))
