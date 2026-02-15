from typing import Any, Dict, List
from src.core.types import FeedbackInsight, PreferenceUpdate, UserFeedback
from src.utils.logger import logger

class InsightExtractor:
    """
    Analyzes historical feedback to identify recurring patterns and actionable insights.

    This component helps the agent transition from item-specific feedback to
    systemic behavioral improvements.
    """

    async def extract_insights(
        self,
        user_id: str,
        feedback: UserFeedback,
        preference_updates: List[PreferenceUpdate],
        recent_feedback: List[Dict[str, Any]]
    ) -> List[FeedbackInsight]:
        """
        Aggregates data from current and historical feedback to generate insights.

        Args:
            user_id (str): User identifier.
            feedback (UserFeedback): The feedback object being currently processed.
            preference_updates (List[PreferenceUpdate]): Updates identified in the current cycle.
            recent_feedback (List[Dict[str, Any]]): Historical feedback items for pattern detection.

        Returns:
            List[FeedbackInsight]: A collection of actionable insights with confidence scores.
        """
        insights = []

        # 1. Convert preference updates to insights
        for update in preference_updates:
            insights.append(FeedbackInsight(
                insight=f"User preference identified: {update.field}",
                confidence=update.confidence,
                action=f"Set default {update.field} to '{update.new_value}'",
                category="preference",
                metadata={"field": update.field, "new_value": update.new_value}
            ))

        # 2. Analyze recurring patterns from history
        if len(recent_feedback) >= 3:
            pattern_insights = self._analyze_patterns(recent_feedback)
            insights.extend(pattern_insights)

        # 3. Category-specific logic
        if "accuracy" in feedback.categories and feedback.sentiment == "negative":
            insights.append(FeedbackInsight(
                insight="User reported accuracy issues",
                confidence=0.85,
                action="Increase validation rigor and fact-checking",
                category="quality"
            ))

        return insights

    def _analyze_patterns(self, history: List[Dict[str, Any]]) -> List[FeedbackInsight]:
        """
        Internal logic for identifying recurring issues across multiple tasks.

        Args:
            history (List[Dict[str, Any]]): Recent feedback history.

        Returns:
            List[FeedbackInsight]: Insights derived from historical trends.
        """
        category_counts = {}
        for fb in history:
            for cat in fb.get("categories", []):
                if fb.get("sentiment") == "negative":
                    category_counts[cat] = category_counts.get(cat, 0) + 1

        insights = []
        for cat, count in category_counts.items():
            if count >= 2:
                insights.append(FeedbackInsight(
                    insight=f"Recurring issue with {cat}",
                    confidence=0.8,
                    action=f"Prioritize improvements in {cat} workflow",
                    category="recurring_pattern"
                ))
        return insights

    def generate_recommendations(self, insights: List[FeedbackInsight]) -> List[str]:
        """
        Translates raw insights into high-level recommendations for future behavior.

        Args:
            insights (List[FeedbackInsight]): The insights to be summarized.

        Returns:
            List[str]: A list of actionable recommendation strings.
        """
        return [i.action for i in insights if i.confidence >= 0.8]
