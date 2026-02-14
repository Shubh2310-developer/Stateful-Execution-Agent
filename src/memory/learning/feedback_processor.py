from typing import Dict, Any, Optional
from src.core.types import TaskState
from src.utils.logger import logger

class FeedbackProcessor:
    """Processes explicit user feedback to adjust future agent behavior."""

    async def process_feedback(self, task_id: str, feedback: Dict[str, Any]):
        logger.info(f"Processing feedback for task {task_id}: {feedback.get('rating')}/5")

        # In a real system, this would influence long-term weights or preferences
        rating = feedback.get("rating", 0)
        comments = feedback.get("comments", "")

        processed = {
            "task_id": task_id,
            "sentiment": "positive" if rating >= 4 else "negative" if rating <= 2 else "neutral",
            "extracted_preferences": self._extract_preferences(comments)
        }
        return processed

    def _extract_preferences(self, text: str) -> Dict[str, Any]:
        """Simple heuristic extraction of preferences from feedback text."""
        prefs = {}
        text_lower = text.lower()
        if "shorter" in text_lower or "brief" in text_lower:
            prefs["detail_level"] = "concise"
        elif "more detail" in text_lower:
            prefs["detail_level"] = "comprehensive"
        return prefs
