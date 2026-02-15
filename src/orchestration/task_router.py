from typing import Any, Dict, Optional, List
from src.orchestration.session_manager import SessionManager
from src.orchestration.workflow_engine import WorkflowEngine
from src.orchestration.state_validator import StateValidator
from src.tools.tool_selector import ToolSelector
from src.core.types import TaskState, TaskStatus
from src.utils.logger import logger

class TaskRouter:
    """Main entry point for routing task requests to appropriate handlers."""

    def __init__(self):
        self.session_manager = SessionManager()
        self.workflow_engine = WorkflowEngine()
        self.state_validator = StateValidator()
        self.tool_selector = ToolSelector()

    async def initialize_task(self, user_id: str, goal: str) -> TaskState:
        import uuid
        task_id = f"task_{uuid.uuid4().hex[:8]}"
        logger.info(f"Initializing new task: {task_id} for user {user_id}")
        # Goal is expected as a Dict for the session manager's initialize_state which creates a Goal object
        state = await self.session_manager.create_session(task_id, user_id, {"request": goal, "success_criteria": []})
        return state

    async def run_task_cycle(self, task_id: str):
        logger.info(f"Starting task cycle for {task_id}")
        state = await self.session_manager.get_session(task_id)
        if not state:
            logger.error(f"Task {task_id} not found for execution")
            return

        try:
            available_tools = self.tool_selector.get_available_tool_names()
            # The workflow engine handles the state transition and execution logic
            await self.workflow_engine.process_task(state, available_tools)
        except Exception as e:
            logger.exception(f"Error in task cycle for {task_id}")
            state.status = TaskStatus.FAILED
            state.metadata["error"] = str(e)
            # Ensure error is saved
            await self.session_manager.state_manager.save_state(state)
        finally:
            await self.session_manager.close_session(task_id)

    async def handle_continuation(self, task_id: str, user_input: Optional[str] = None, mode: str = "resume") -> TaskState:
        logger.info(f"Handling continuation for task {task_id} with mode {mode}")
        state = await self.session_manager.get_session(task_id)
        if not state:
            raise ValueError(f"Task {task_id} not found")

        if mode == "restart":
            state.status = TaskStatus.PENDING
            state.current_step_index = 0
            state.plan = None
            state.artifacts = []
            state.logs = []
        elif mode == "modify_plan":
            state.status = TaskStatus.PLANNING
            if user_input:
                state.metadata["plan_modification_request"] = user_input
        else:  # resume
            if state.status in [TaskStatus.PAUSED, TaskStatus.FAILED]:
                state.status = TaskStatus.EXECUTING
            if user_input:
                state.metadata["user_feedback"] = user_input

        # Save the updated state before background task takes over
        await self.session_manager.state_manager.save_state(state)
        return state
