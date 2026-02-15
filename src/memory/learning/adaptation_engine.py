from typing import Dict, Any, List, Optional
from src.core.types import TaskState, UserMemory, TaskStatus, HistoricalPattern
from src.llm.groq_client import groq_client
from src.llm.prompt_builder import prompt_builder
from src.llm.response_parser import ResponseParser
from src.utils.logger import logger
from src.memory.memory_manager import MemoryManager
from src.memory.retrieval.semantic_search import SemanticSearch

class AdaptationEngine:
    """
    Engine responsible for post-task reflection and long-term learning.

    This component analyzes the execution trace, produced artifacts, and user feedback
    to extract lessons learned and update the agent's historical knowledge base.
    """

    def __init__(self, memory_manager: Optional[MemoryManager] = None):
        """
        Initializes the AdaptationEngine.

        Args:
            memory_manager (MemoryManager, optional): Manager for persistent memory operations.
                Defaults to a new MemoryManager instance.
        """
        self.memory_manager = memory_manager or MemoryManager()
        self.semantic_search = SemanticSearch(self.memory_manager)

    async def learn_from_task(self, state: TaskState, feedback: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Triggers a deep reflection process on a completed or failed task.

        Args:
            state (TaskState): The final state of the task, including logs and artifacts.
            feedback (Dict[str, Any], optional): User feedback processed by FeedbackProcessor.
                Defaults to None.

        Returns:
            Dict[str, Any]: A summary of the reflection process, including identified
                lessons learned and potential improvements for future similar tasks.
        """
        logger.info(f"Triggering deep reflection for task: {state.task_id}")

        if state.status != TaskStatus.COMPLETED and state.status != TaskStatus.FAILED:
            logger.warning(f"Task {state.task_id} is in status {state.status}, reflection might be premature.")

        # 1. Prepare context for Reflection
        artifacts_data = [
            {"id": a.id, "type": a.type, "uri": a.uri}
            for a in state.artifacts
        ]

        # Intelligent log summarization to prevent token overflow
        logs_data = []
        max_logs = 15

        if len(state.logs) > max_logs:
            logger.info(f"Task has {len(state.logs)} logs. Summarizing to top/bottom {max_logs//2} logs.")
            # Keep first few and last few logs as they are usually most informative for overall flow and final outcome
            head_logs = state.logs[:max_logs//2]
            tail_logs = state.logs[-(max_logs//2):]

            for l in head_logs:
                logs_data.append(self._format_log(l))

            logs_data.append({
                "step_id": "...",
                "action": "SUMMARIZED",
                "description": f"... {len(state.logs) - max_logs} steps omitted for brevity ...",
                "output": "..."
            })

            for l in tail_logs:
                logs_data.append(self._format_log(l))
        else:
            for l in state.logs:
                logs_data.append(self._format_log(l))

        messages = prompt_builder.build_reflection_prompt(
            goal=state.goal.request,
            status=state.status.value,
            logs=logs_data,
            artifacts=artifacts_data,
            feedback=feedback
        )

        try:
            response = await groq_client.generate_response(
                messages=messages,
                temperature=0.5,
                max_tokens=2000
            )
            
            parser = ResponseParser()
            reflection_summary = parser.parse_json_response(response)
            
            logger.info(f"Reflection complete for task {state.task_id}")
            return reflection_summary

        except Exception as e:
            logger.error(f"Reflection loop failed for task {state.task_id}: {str(e)}")
            return {}

    def _format_log(self, log: Any) -> Dict[str, Any]:
        """Formats a single log entry for the reflection prompt."""
        return {
            "step_id": log.step_id,
            "action": log.action,
            "description": log.description,
            "output": str(log.output)[:1000] if log.output else "None"
        }
