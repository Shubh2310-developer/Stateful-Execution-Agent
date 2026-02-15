from typing import Any, Dict, List, Optional
from src.core.types import TaskState
from src.utils.logger import logger
from src.llm.groq_client import groq_client
from src.llm.prompt_builder import prompt_builder
from src.llm.response_parser import ResponseParser
from src.executor.artifact_manager import ArtifactManager

class SuccessValidator:
    """
    Component responsible for determining if a task has achieved its primary objective.

    It provides two layers of validation:
    1. Static: Fast check based on plan completion and artifact counts.
    2. Semantic (LLM): Deep evaluation comparing final output against success criteria.
    """

    def __init__(self):
        """Initializes the SuccessValidator with access to artifact management."""
        self.artifact_manager = ArtifactManager()

    def validate_achievement(self, state: TaskState) -> Dict[str, Any]:
        """
        Performs a fast, static validation of goal achievement.

        Checks if the current step index matches the total steps in the plan and
        verifies that at least one artifact was produced.

        Args:
            state (TaskState): The current state of the task being validated.

        Returns:
            Dict[str, Any]: Dictionary containing achievement status, ratio, and
                the reason for the determination.
        """
        logger.info(f"Validating goal achievement for task: {state.task_id}")

        # Check if all steps are completed
        total_steps = len(state.plan.steps) if state.plan else 0
        completed_steps = state.current_step_index

        if total_steps == 0:
            return {"achieved": False, "reason": "No plan exists"}

        achievement_ratio = completed_steps / total_steps

        # Check for presence of final artifacts
        has_artifacts = len(state.artifacts) > 0

        achieved = achievement_ratio >= 1.0 and has_artifacts

        return {
            "achieved": achieved,
            "achievement_ratio": achievement_ratio,
            "artifacts_count": len(state.artifacts),
            "reason": "All steps completed" if achieved else "Incomplete steps or missing artifacts"
        }

    async def validate_achievement_llm(self, state: TaskState) -> Dict[str, Any]:
        """
        Performs a semantic evaluation of goal achievement using an LLM.

        This method retrieves the content of all produced artifacts and asks an LLM
        to judge them against the original goal request and success criteria.

        Args:
            state (TaskState): The current state of the task, containing goals
                and artifacts.

        Returns:
            Dict[str, Any]: A detailed assessment from the LLM including a
                completion score and qualitative reasoning.
        """
        logger.info(f"Performing LLM-powered success validation for task: {state.task_id}")

        # 1. Prepare artifact content previews
        artifact_previews = []
        for artifact in state.artifacts:
            try:
                content = self.artifact_manager.get_artifact_content(artifact)
                artifact_previews.append({
                    "id": artifact.id,
                    "type": artifact.type,
                    "content": str(content)[:2000] # Limit context window usage
                })
            except Exception as e:
                logger.warning(f"Could not load content for artifact {artifact.id}: {e}")

        # 2. Build validation prompt
        # We reuse the validator templates but focused on the overall goal
        messages = [
            {
                "role": "system",
                "content": "You are a Goal Achievement Auditor. Your task is to compare the produced artifacts against the original goal and success criteria to determine if the objective was fully met."
            },
            {
                "role": "user",
                "content": f"Goal: {state.goal.request}\n\nSuccess Criteria: {state.goal.success_criteria}\n\nProduced Artifacts: {artifact_previews}\n\nDetermine if the goal was achieved. Return a JSON object with 'achieved' (bool), 'completion_score' (0.0-1.0), and 'reasoning' (string)."
            }
        ]

        try:
            response_text = await groq_client.generate_response(messages, temperature=0.2)
            result = ResponseParser.parse_json_response(response_text)

            logger.info(f"LLM Success Validation Result: {result.get('achieved')} (Score: {result.get('completion_score')})")
            return result
        except Exception as e:
            logger.error(f"LLM success validation failed: {e}")
            # Fallback to static validation
            return self.validate_achievement(state)
