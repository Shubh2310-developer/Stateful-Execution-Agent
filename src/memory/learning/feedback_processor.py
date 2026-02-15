from typing import Dict, Any, Optional, List
from datetime import datetime, timezone
import shortuuid

from src.core.types import TaskState, UserMemory, UserPreferences, HistoricalPattern, UserFeedback
from src.state.persistence.database_adapter import DatabaseAdapter
from src.memory.learning.sentiment_analyzer import SentimentAnalyzer
from src.memory.learning.preference_manager import PreferenceManager
from src.memory.learning.insight_extractor import InsightExtractor
from src.utils.logger import logger

class FeedbackProcessor:
    """
    Orchestrates the processing of user feedback to adjust future agent behavior.

    This class coordinates sentiment analysis, preference management, and
    insight extraction into a single pipeline.
    """

    def __init__(self, db_adapter: Optional[DatabaseAdapter] = None):
        self.db_adapter = db_adapter or DatabaseAdapter()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.preference_manager = PreferenceManager(self.db_adapter.db.user_profiles)
        self.insight_extractor = InsightExtractor()

        self.feedback_collection = self.db_adapter.db.user_feedback
        self.patterns_collection = self.db_adapter.db.historical_patterns

    async def process_feedback(
        self,
        task_id: str,
        user_id: str,
        rating: int,
        text_feedback: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Complete feedback processing pipeline.
        """
        logger.info(f"Processing feedback for task {task_id}: rating={rating}/5")

        try:
            # 1. Initialize feedback object
            sentiment = self.sentiment_analyzer.parse_rating(rating)
            feedback_id = f"fb_{shortuuid.uuid()[:12]}"

            categories = []
            if text_feedback:
                parsed_data = await self.sentiment_analyzer.parse_text_feedback(text_feedback)
                categories = parsed_data.get("categories", [])

            # 2. Update user preferences
            preference_updates = []
            if text_feedback:
                preference_updates = self.preference_manager.identify_updates(text_feedback, rating)
                await self.preference_manager.apply_updates(user_id, preference_updates)

            # 3. Update historical patterns
            pattern_updated = await self._update_historical_patterns(
                user_id, task_id, rating, categories, text_feedback
            )

            # 4. Extract actionable insights
            recent_feedback = await self.get_recent_feedback(user_id, limit=10)

            # Create a temporary UserFeedback-like object for extractor
            temp_feedback = UserFeedback(
                feedback_id=feedback_id,
                task_id=task_id,
                user_id=user_id,
                rating=rating,
                text_feedback=text_feedback,
                sentiment=sentiment,
                categories=categories
            )

            insights = await self.insight_extractor.extract_insights(
                user_id, temp_feedback, preference_updates, recent_feedback
            )
            recommendations = self.insight_extractor.generate_recommendations(insights)

            # 5. Save feedback to MongoDB
            feedback_doc = temp_feedback.model_dump()
            await self.feedback_collection.insert_one(feedback_doc)

            return {
                "feedback_id": feedback_id,
                "processed_at": datetime.now(timezone.utc).isoformat(),
                "sentiment": sentiment,
                "categories": categories,
                "preference_updates": [u.model_dump() for u in preference_updates],
                "historical_pattern_updated": pattern_updated,
                "insights": [i.model_dump() for i in insights],
                "recommendations_for_future": recommendations
            }

        except Exception as e:
            logger.error(f"Failed to process feedback: {str(e)}", exc_info=True)
            return {
                "error": str(e),
                "task_id": task_id,
                "processed_at": datetime.now(timezone.utc).isoformat()
            }

    async def _update_historical_patterns(
        self,
        user_id: str,
        task_id: str,
        rating: int,
        categories: List[str],
        text_feedback: Optional[str]
    ) -> bool:
        """Create or update HistoricalPattern entry for the task."""
        try:
            task_doc = await self.db_adapter.tasks.find_one({"task_id": task_id})
            if not task_doc:
                return False

            pattern = {
                "user_id": user_id,
                "task_id": task_id,
                "goal_request": task_doc.get("goal", {}).get("request", ""),
                "success_score": rating / 5.0,
                "tags": categories,
                "created_at": datetime.now(timezone.utc)
            }

            await self.patterns_collection.insert_one(pattern)
            return True
        except Exception as e:
            logger.error(f"Failed to update historical patterns: {str(e)}")
            return False

    async def get_recent_feedback(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent feedback items for a user."""
        try:
            cursor = self.feedback_collection.find({"user_id": user_id}).sort("timestamp", -1).limit(limit)
            return await cursor.to_list(length=limit)
        except Exception as e:
            logger.error(f"Failed to retrieve recent feedback: {str(e)}")
            return []
