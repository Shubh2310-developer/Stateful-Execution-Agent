from typing import Dict, Any, List, Optional
from src.core.types import TaskState, UserMemory, TaskStatus, HistoricalPattern
from src.llm.groq_client import groq_client
from src.llm.prompt_builder import prompt_builder
from src.llm.response_parser import ResponseParser
from src.utils.logger import logger
from src.memory.memory_manager import MemoryManager
from src.memory.retrieval.semantic_search import SemanticSearch

class AdaptationEngine:
    """Extracts lessons from completed tasks to update long-term memory."""

    def __init__(self, memory_manager: Optional[MemoryManager] = None):
        self.memory_manager = memory_manager or MemoryManager()
        self.semantic_search = SemanticSearch(self.memory_manager)

    async def learn_from_task(self, state: TaskState, feedback: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        logger.info(f"Triggering deep reflection for task: {state.task_id}")

        if state.status != TaskStatus.COMPLETED and state.status != TaskStatus.FAILED:
            logger.warning(f"Task {state.task_id} is in status {state.status}, reflection might be premature.")

        # 1. Prepare context for Reflection
        artifacts_data = [
            {"id": a.id, "type": a.type, "uri": a.uri}
            for a in state.artifacts
        ]

        logs_data = [
            {
                "step_id": l.step_id,
                "action": l.action,
                "description": l.description,
                "output": str(l.output)[:1000] # Truncate large outputs
            }
            for l in state.logs
        ]

        messages = prompt_builder.build_reflection_prompt(
            goal=state.goal.request,
            status=state.status.value,
            logs=logs_data,
            artifacts=artifacts_data,
            feedback=feedback
        )

        try:
            # 2. Call LLM for Reflection
            response_text = await groq_client.generate_response(messages)
            reflection_summary = ResponseParser.parse_json_response(response_text)

            logger.info(f"Reflection completed for task {state.task_id}")
            if "reasoning" in reflection_summary:
                logger.debug(f"Reflection Reasoning: {reflection_summary['reasoning']}")

            # 3. Update User Preferences
            pref_updates = reflection_summary.get("user_preference_updates")
            if pref_updates:
                logger.info(f"Updating user preferences from reflection: {list(pref_updates.keys())}")
                await self.memory_manager.update_user_preferences(state.user_id, pref_updates)

            # 4. Store Historical Pattern
            patterns_data = reflection_summary.get("patterns")
            if patterns_data:
                # Combine insights and corrections into metadata
                combined_lessons = reflection_summary.get("insights", []) + reflection_summary.get("corrections", [])

                embedding_text = f"Goal: {state.goal.request}\nApproach: {patterns_data.get('successful_approach', '')}"
                embedding = self.semantic_search.generate_embedding(embedding_text)

                pattern = HistoricalPattern(
                    user_id=state.user_id,
                    task_id=state.task_id,
                    goal_request=state.goal.request,
                    plan_summary=patterns_data.get("task_category", "general"),
                    approach=patterns_data.get("successful_approach"),
                    outcome=state.status.value,
                    success_score=patterns_data.get("confidence_score", 1.0 if state.status == TaskStatus.COMPLETED else 0.0),
                    tags=combined_lessons,
                    embedding=embedding,
                    metadata={
                        "reflection_reasoning": reflection_summary.get("reasoning"),
                        "insights": reflection_summary.get("insights", []),
                        "corrections": reflection_summary.get("corrections", [])
                    }
                )
                await self.memory_manager.add_historical_pattern(pattern)
                logger.info(f"Stored historical pattern for task {state.task_id}")

            return reflection_summary

        except Exception as e:
            logger.error(f"Reflection loop failed for task {state.task_id}: {str(e)}")
            return {}
