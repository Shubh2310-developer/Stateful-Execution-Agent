from typing import Any, Dict, Optional, List
from src.llm.groq_client import groq_client
from src.llm.response_parser import ResponseParser
from src.core.exceptions import LLMError
from src.utils.logger import logger

class SentimentAnalyzer:
    """
    Handles sentiment analysis and structured data extraction from user feedback.

    Uses LLM-powered parsing for deep understanding of text feedback with a
    fallback to keyword-based heuristics.
    """

    def parse_rating(self, rating: int) -> str:
        """
        Maps a numeric 1-5 rating to a categorical sentiment string.

        Args:
            rating (int): Rating on a 1-5 scale.

        Returns:
            str: One of "positive", "neutral", or "negative".
        """
        if not 1 <= rating <= 5:
            logger.warning(f"Invalid rating {rating}, defaulting to neutral")
            return "neutral"
        if rating >= 4:
            return "positive"
        elif rating <= 2:
            return "negative"
        else:
            return "neutral"

    async def parse_text_feedback(self, text_feedback: str) -> Dict[str, Any]:
        """
        Uses an LLM to extract structured categories and sentiment from raw text.

        Args:
            text_feedback (str): The raw text provided by the user.

        Returns:
            Dict[str, Any]: Structured data containing identified categories,
                specific quality issues, and preference signals.
        """
        try:
            from src.llm.prompt_builder import prompt_builder
            messages = prompt_builder.build_feedback_parser_prompt(text_feedback)
            response = await groq_client.generate_response(
                messages=messages,
                temperature=0.3,
                max_tokens=1024
            )
            return ResponseParser.parse_json_response(response)
        except Exception as e:
            logger.warning(f"LLM parsing failed, using heuristics: {str(e)}")
            return self._heuristic_parse(text_feedback)

    def _heuristic_parse(self, text: str) -> Dict[str, Any]:
        """
        Fallback keyword-based parser for user feedback.

        Args:
            text (str): The raw feedback text.

        Returns:
            Dict[str, Any]: Heuristically identified metadata.
        """
        text_lower = text.lower()
        categories = []
        quality_issues = []

        mapping = {
            "speed": ["fast", "slow", "speed", "quick", "time"],
            "accuracy": ["accurate", "correct", "wrong", "error", "mistake"],
            "format": ["format", "layout", "structure", "pdf", "markdown"],
            "tone": ["tone", "professional", "casual", "formal"],
            "completeness": ["complete", "incomplete", "missing", "lacking"],
            "clarity": ["clear", "unclear", "confusing", "vague"]
        }

        for cat, keywords in mapping.items():
            if any(word in text_lower for word in keywords):
                categories.append(cat)

        if any(word in text_lower for word in ["missing", "lacking", "incomplete"]):
            quality_issues.append("incomplete output")
        if any(word in text_lower for word in ["error", "wrong", "incorrect", "mistake"]):
            quality_issues.append("accuracy issues")

        return {
            "sentiment_aspects": {"positive": [], "negative": quality_issues},
            "categories": categories,
            "quality_issues": quality_issues,
            "preference_signals": []
        }
