from typing import Any, Dict, List, Optional
from src.core.types import Step, Artifact, Decision, UserMemory
from src.executor.tool_orchestrator import ToolOrchestrator
from src.executor.artifact_manager import ArtifactManager
from src.llm.groq_client import groq_client
from src.llm.prompt_builder import prompt_builder
from src.llm.response_parser import ResponseParser
from src.utils.logger import logger
from datetime import datetime
from uuid import uuid4

class StepRunner:
    """Executes a single step from the plan, coordinating tools and state."""

    def __init__(self, artifact_manager: ArtifactManager):
        self.tool_orchestrator = ToolOrchestrator()
        self.artifact_manager = artifact_manager

    async def run_step(
        self,
        task_id: str,
        step: Step,
        available_artifacts: Dict[str, Artifact],
        user_memory: Optional[UserMemory] = None
    ) -> Dict[str, Any]:
        step_id = getattr(step, 'id', getattr(step, 'step_id', 'unknown'))
        action_name = getattr(step, 'action', 'unknown')

        logger.info(f"Running step {step_id}: {action_name}")

        # 1. Prepare context for LLM
        artifact_contents = {
            art_id: self.artifact_manager.get_artifact_content(art)
            for art_id, art in available_artifacts.items()
        }

        messages = prompt_builder.build_executor_prompt(
            step=step,
            available_artifacts=artifact_contents,
            tool_list=self.tool_orchestrator.tool_selector.get_available_tool_names(),
            user_preferences=getattr(user_memory, 'preferences', None) if user_memory else None,
            include_examples=True
        )

        # 2. Get tool parameters from LLM
        response_text = await groq_client.generate_response(messages)
        execution_decision = ResponseParser.parse_json_response(response_text)

        action, params = ResponseParser.extract_action_and_params(execution_decision)
        reasoning = execution_decision.get("reasoning", "Executing as planned.")

        # 3. Invoke Tool
        start_time = datetime.utcnow()
        tool_output = await self.tool_orchestrator.invoke_tool(action, params)
        end_time = datetime.utcnow()

        # 4. Record Decision
        decision = Decision(
            decision_id=f"dec_{uuid4().hex[:8]}",
            task_id=task_id,
            step_id=step_id,
            timestamp=datetime.utcnow(),
            decision_point=f"Execution of {step_id}",
            reasoning=reasoning,
            choice_made=action,
            confidence=execution_decision.get("confidence", 1.0),
            impact="medium"
        )

        # 5. Create Artifact
        artifact = await self.artifact_manager.create_artifact(
            task_id=task_id,
            step_id=step_id,
            artifact_type="data",
            content=tool_output,
            format="json"
        )

        return {
            "status": "completed",
            "artifact": artifact,
            "decision": decision,
            "duration": (end_time - start_time).total_seconds()
        }
