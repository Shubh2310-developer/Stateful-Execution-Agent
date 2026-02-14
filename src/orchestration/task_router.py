from typing import Any, Dict, Optional
from src.orchestration.session_manager import SessionManager
from src.orchestration.workflow_engine import WorkflowEngine
from src.orchestration.state_validator import StateValidator
from src.tools.tool_selector import ToolSelector
from src.utils.logger import logger

class TaskRouter:
    """Main entry point for routing task requests to appropriate handlers."""

    def __init__(self):
        self.session_manager = SessionManager()
        self.workflow_engine = WorkflowEngine()
        self.state_validator = StateValidator()
        self.tool_selector = ToolSelector()

    async def handle_request(self, user_id: str, goal: str, task_id: Optional[str] = None) -> Dict[str, Any]:
        if task_id:
            logger.info(f"Routing continuation request for task {task_id}")
            state = await self.session_manager.get_session(task_id)
        else:
            import uuid
            task_id = f"task_{uuid.uuid4().hex[:8]}"
            logger.info(f"Routing new task request: {task_id}")
            state = await self.session_manager.create_session(task_id, user_id, {"request": goal})

        # Process through workflow engine
        available_tools = self.tool_selector.get_available_tool_names()
        updated_state = await self.workflow_engine.process_task(state, available_tools)

        # Save and close session
        await self.session_manager.close_session(task_id)

        return updated_state.dict()
