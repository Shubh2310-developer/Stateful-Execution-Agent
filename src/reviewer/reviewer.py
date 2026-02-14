from typing import Any, Dict, Optional
from src.core.types import TaskState
from src.reviewer.quality_checker import QualityChecker
from src.reviewer.success_validator import SuccessValidator
from src.executor.artifact_manager import ArtifactManager
from src.utils.logger import logger
from src.llm.prompt_builder import prompt_builder
from src.llm.groq_client import groq_client
from src.llm.response_parser import ResponseParser

class Reviewer:
    """Orchestrates the review and validation of task execution."""

    def __init__(self):
        self.quality_checker = QualityChecker()
        self.success_validator = SuccessValidator()
        self.artifact_manager = ArtifactManager()

    async def review_task(self, state: TaskState) -> Dict[str, Any]:
        logger.info(f"Starting review for task: {state.task_id}")

        # 1. Collect artifacts content
        artifact_list = []
        for artifact in state.artifacts:
            # We include metadata for all, but content only for key types
            art_data = artifact.dict()
            if artifact.type in ["document", "data", "code"]:
                art_data["content_preview"] = str(self.artifact_manager.get_artifact_content(artifact))[:2000]
            artifact_list.append(art_data)

        # 2. Build and run end-to-end review prompt
        messages = prompt_builder.build_reviewer_prompt(
            goal=state.goal.dict(),
            plan_steps=[s.dict() for s in state.plan.steps] if state.plan else [],
            artifacts=artifact_list
        )

        try:
            response_text = await groq_client.generate_response(messages)
            review_result = ResponseParser.parse_json_response(response_text)

            # Log the Chain-of-Thought reasoning
            reasoning = review_result.get("reasoning", "No reasoning provided.")
            logger.info(f"Reviewer Reasoning: {reasoning}")

            # 3. Check individual artifact quality as a secondary check if needed
            quality_reports = {}
            for artifact in state.artifacts:
                if artifact.type in ["document", "data", "code"]:
                    content = self.artifact_manager.get_artifact_content(artifact)
                    report = await self.quality_checker.check_quality(artifact, content)
                    quality_reports[artifact.id] = report

            return {
                "task_id": state.task_id,
                "overall_success": review_result.get("overall_success", False),
                "quality_score": review_result.get("quality_score", 0.0),
                "feedback": review_result.get("feedback", ""),
                "recommendations": review_result.get("recommendations", []),
                "artifact_quality": quality_reports,
                "reasoning": reasoning
            }
        except Exception as e:
            logger.error(f"End-to-end review failed: {str(e)}")
            return {
                "task_id": state.task_id,
                "overall_success": False,
                "error": str(e)
            }
