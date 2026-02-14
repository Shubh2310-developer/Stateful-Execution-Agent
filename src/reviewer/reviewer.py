from typing import Any, Dict, Optional
from src.core.types import TaskState
from src.reviewer.quality_checker import QualityChecker
from src.reviewer.success_validator import SuccessValidator
from src.executor.artifact_manager import ArtifactManager
from src.utils.logger import logger

class Reviewer:
    """Orchestrates the review and validation of task execution."""

    def __init__(self):
        self.quality_checker = QualityChecker()
        self.success_validator = SuccessValidator()
        self.artifact_manager = ArtifactManager()

    async def review_task(self, state: TaskState) -> Dict[str, Any]:
        logger.info(f"Starting review for task: {state.task_id}")

        # 1. Validate overall achievement
        success_report = self.success_validator.validate_achievement(state)

        # 2. Check quality of the final/most important artifacts
        quality_reports = {}
        for art_id, artifact in state.artifacts.items():
            # Only check high-level artifacts for now
            if artifact.type in ["document", "data"]:
                content = self.artifact_manager.get_artifact_content(artifact)
                report = await self.quality_checker.check_quality(artifact, content)
                quality_reports[art_id] = report

        return {
            "task_id": state.task_id,
            "success": success_report,
            "artifact_quality": quality_reports,
            "overall_status": "approved" if success_report["achieved"] else "pending_revision"
        }
