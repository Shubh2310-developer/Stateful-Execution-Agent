import pytest
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch
from typing import Dict, Any, List

from src.memory.learning.feedback_processor import (
    FeedbackProcessor,
    UserFeedback,
    PreferenceUpdate,
    FeedbackInsight,
    FeedbackProcessingResult
)
from src.core.types import UserPreferences


@pytest.fixture
def mock_db_adapter():
    """Create a mock database adapter."""
    adapter = AsyncMock()
    adapter.db = MagicMock()
    adapter.db.user_feedback = AsyncMock()
    adapter.db.user_profiles = AsyncMock()
    adapter.db.historical_patterns = AsyncMock()
    adapter.tasks = AsyncMock()
    adapter.traces = AsyncMock()
    adapter.decisions = AsyncMock()
    return adapter


@pytest.fixture
def feedback_processor(mock_db_adapter):
    """Create a FeedbackProcessor instance with mocked dependencies."""
    return FeedbackProcessor(db_adapter=mock_db_adapter)


class TestRatingParsing:
    """Test rating parsing functionality."""

    def test_parse_rating_positive(self, feedback_processor):
        """Test parsing positive ratings (4-5)."""
        assert feedback_processor.parse_rating(5) == "positive"
        assert feedback_processor.parse_rating(4) == "positive"

    def test_parse_rating_neutral(self, feedback_processor):
        """Test parsing neutral rating (3)."""
        assert feedback_processor.parse_rating(3) == "neutral"

    def test_parse_rating_negative(self, feedback_processor):
        """Test parsing negative ratings (1-2)."""
        assert feedback_processor.parse_rating(2) == "negative"
        assert feedback_processor.parse_rating(1) == "negative"

    def test_parse_rating_invalid(self, feedback_processor):
        """Test handling invalid ratings."""
        assert feedback_processor.parse_rating(0) == "neutral"
        assert feedback_processor.parse_rating(6) == "neutral"
        assert feedback_processor.parse_rating(-1) == "neutral"


class TestHeuristicParsing:
    """Test heuristic-based feedback parsing."""

    def test_parse_speed_category(self, feedback_processor):
        """Test detection of speed-related feedback."""
        feedback = "The task was too slow"
        result = feedback_processor._heuristic_parse_feedback(feedback)
        assert "speed" in result["categories"]

    def test_parse_accuracy_category(self, feedback_processor):
        """Test detection of accuracy-related feedback."""
        feedback = "There were several errors in the output"
        result = feedback_processor._heuristic_parse_feedback(feedback)
        assert "accuracy" in result["categories"]

    def test_parse_format_category(self, feedback_processor):
        """Test detection of format-related feedback."""
        feedback = "I prefer markdown over PDF format"
        result = feedback_processor._heuristic_parse_feedback(feedback)
        assert "format" in result["categories"]

    def test_parse_concise_preference(self, feedback_processor):
        """Test detection of concise preference."""
        feedback = "The response was too verbose, please be more brief"
        result = feedback_processor._heuristic_parse_feedback(feedback)
        assert any("concise" in signal for signal in result["preference_signals"])

    def test_parse_comprehensive_preference(self, feedback_processor):
        """Test detection of comprehensive preference."""
        feedback = "I need more detail and thorough analysis"
        result = feedback_processor._heuristic_parse_feedback(feedback)
        assert any("comprehensive" in signal for signal in result["preference_signals"])

    def test_parse_citation_preference(self, feedback_processor):
        """Test detection of citation preference."""
        feedback = "Please include citations and sources"
        result = feedback_processor._heuristic_parse_feedback(feedback)
        assert any("citation" in signal for signal in result["preference_signals"])

    def test_parse_multiple_categories(self, feedback_processor):
        """Test parsing feedback with multiple categories."""
        feedback = "The output was slow, had errors, and unclear formatting"
        result = feedback_processor._heuristic_parse_feedback(feedback)
        assert "speed" in result["categories"]
        assert "accuracy" in result["categories"]
        assert "format" in result["categories"]


class TestTextFeedbackParsing:
    """Test LLM-based text feedback parsing."""

    @pytest.mark.asyncio
    async def test_parse_text_feedback_with_llm(self, feedback_processor):
        """Test successful LLM parsing of text feedback."""
        mock_response = """{
            "sentiment_aspects": {
                "positive": ["good structure"],
                "negative": ["too long"]
            },
            "preference_signals": ["prefers concise"],
            "quality_issues": [],
            "categories": ["format", "completeness"],
            "specific_mentions": ["step 2"]
        }"""

        with patch('src.memory.learning.feedback_processor.groq_client') as mock_client:
            mock_client.generate_response = AsyncMock(return_value=mock_response)

            result = await feedback_processor.parse_text_feedback("The output was good but too long")

            assert "categories" in result
            assert "format" in result["categories"]
            assert "preference_signals" in result

    @pytest.mark.asyncio
    async def test_parse_text_feedback_llm_fallback(self, feedback_processor):
        """Test fallback to heuristics when LLM fails."""
        with patch('src.memory.learning.feedback_processor.groq_client') as mock_client:
            mock_client.generate_response = AsyncMock(side_effect=Exception("LLM Error"))

            result = await feedback_processor.parse_text_feedback("Too slow and errors")

            # Should fall back to heuristic parsing
            assert "categories" in result
            assert "speed" in result["categories"] or "accuracy" in result["categories"]


class TestCorrelationAnalysis:
    """Test feedback correlation to execution traces."""

    @pytest.mark.asyncio
    async def test_correlate_with_no_trace_data(self, feedback_processor, mock_db_adapter):
        """Test correlation when no trace data exists."""
        mock_db_adapter.traces.find.return_value.sort.return_value.to_list = AsyncMock(return_value=[])
        mock_db_adapter.decisions.find.return_value.sort.return_value.to_list = AsyncMock(return_value=[])

        result = await feedback_processor.correlate_feedback_to_execution(
            "task_123", "negative", "The output was wrong"
        )

        assert result["steps"] == {}
        assert result["decisions"] == {}

    @pytest.mark.asyncio
    async def test_heuristic_correlate_negative_sentiment(self, feedback_processor):
        """Test heuristic correlation for negative sentiment."""
        traces = []
        decisions = [
            {"decision_id": "dec_1", "confidence_score": 0.5},
            {"decision_id": "dec_2", "confidence_score": 0.9}
        ]

        result = feedback_processor._heuristic_correlate("negative", traces, decisions)

        # Should correlate to low-confidence decision
        assert "dec_1" in result["decisions"]
        assert result["decisions"]["dec_1"] == 0.5  # 1.0 - 0.5

    @pytest.mark.asyncio
    async def test_heuristic_correlate_positive_sentiment(self, feedback_processor):
        """Test heuristic correlation for positive sentiment."""
        traces = []
        decisions = [
            {"decision_id": "dec_1", "confidence_score": 0.5},
            {"decision_id": "dec_2", "confidence_score": 0.9}
        ]

        result = feedback_processor._heuristic_correlate("positive", traces, decisions)

        # Should correlate to high-confidence decision
        assert "dec_2" in result["decisions"]
        assert result["decisions"]["dec_2"] == 0.9


class TestPreferenceUpdates:
    """Test user preference updates."""

    @pytest.mark.asyncio
    async def test_update_detail_level_concise(self, feedback_processor, mock_db_adapter):
        """Test updating detail_level to concise."""
        mock_db_adapter.db.user_profiles.find_one = AsyncMock(return_value=None)
        mock_db_adapter.db.user_profiles.update_one = AsyncMock()

        updates = await feedback_processor.update_user_preferences(
            "user_123",
            2,
            "Too verbose, please be more brief",
            []
        )

        assert len(updates) > 0
        assert any(u.field == "detail_level" and u.new_value == "concise" for u in updates)

    @pytest.mark.asyncio
    async def test_update_detail_level_comprehensive(self, feedback_processor, mock_db_adapter):
        """Test updating detail_level to comprehensive."""
        mock_db_adapter.db.user_profiles.find_one = AsyncMock(return_value=None)
        mock_db_adapter.db.user_profiles.update_one = AsyncMock()

        updates = await feedback_processor.update_user_preferences(
            "user_123",
            5,
            "I need more detail and comprehensive analysis",
            []
        )

        assert len(updates) > 0
        assert any(u.field == "detail_level" and u.new_value == "comprehensive" for u in updates)

    @pytest.mark.asyncio
    async def test_update_tone_professional(self, feedback_processor, mock_db_adapter):
        """Test updating tone to professional."""
        mock_db_adapter.db.user_profiles.find_one = AsyncMock(return_value=None)
        mock_db_adapter.db.user_profiles.update_one = AsyncMock()

        updates = await feedback_processor.update_user_preferences(
            "user_123",
            5,
            "Please use a more professional tone",
            []
        )

        assert any(u.field == "document_tone" and u.new_value == "professional" for u in updates)

    @pytest.mark.asyncio
    async def test_update_format_preference(self, feedback_processor, mock_db_adapter):
        """Test updating format preferences."""
        mock_db_adapter.db.user_profiles.find_one = AsyncMock(return_value=None)
        mock_db_adapter.db.user_profiles.update_one = AsyncMock()

        updates = await feedback_processor.update_user_preferences(
            "user_123",
            1,
            "I don't like PDF format",
            []
        )

        assert any(u.field == "preferred_formats" for u in updates)

    @pytest.mark.asyncio
    async def test_update_citation_preference(self, feedback_processor, mock_db_adapter):
        """Test updating citation preferences."""
        mock_db_adapter.db.user_profiles.find_one = AsyncMock(return_value=None)
        mock_db_adapter.db.user_profiles.update_one = AsyncMock()

        updates = await feedback_processor.update_user_preferences(
            "user_123",
            5,
            "Please include citations",
            []
        )

        assert any("citations" in u.field for u in updates)


class TestHistoricalPatterns:
    """Test historical pattern updates."""

    @pytest.mark.asyncio
    async def test_update_historical_patterns_success(self, feedback_processor, mock_db_adapter):
        """Test successful historical pattern update."""
        task_doc = {
            "task_id": "task_123",
            "goal": {"request": "Generate a report"},
            "plan": {"steps": [{"action": "research"}, {"action": "write"}]},
            "status": "COMPLETED",
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        }

        mock_db_adapter.tasks.find_one = AsyncMock(return_value=task_doc)
        mock_db_adapter.db.historical_patterns.insert_one = AsyncMock()

        result = await feedback_processor.update_historical_patterns(
            "user_123",
            "task_123",
            5,
            ["quality", "speed"],
            "Great job!"
        )

        assert result is True
        mock_db_adapter.db.historical_patterns.insert_one.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_historical_patterns_no_task(self, feedback_processor, mock_db_adapter):
        """Test historical pattern update when task not found."""
        mock_db_adapter.tasks.find_one = AsyncMock(return_value=None)

        result = await feedback_processor.update_historical_patterns(
            "user_123",
            "task_123",
            5,
            [],
            None
        )

        assert result is False

    def test_rating_to_success_score(self, feedback_processor):
        """Test conversion of rating to success score."""
        assert feedback_processor._rating_to_success_score(1) == 0.2
        assert feedback_processor._rating_to_success_score(2) == 0.4
        assert feedback_processor._rating_to_success_score(3) == 0.6
        assert feedback_processor._rating_to_success_score(4) == 0.8
        assert feedback_processor._rating_to_success_score(5) == 1.0

    def test_summarize_plan(self, feedback_processor):
        """Test plan summarization."""
        plan = {
            "steps": [
                {"action": "research"},
                {"action": "analyze"},
                {"action": "write"},
                {"action": "review"}
            ]
        }

        summary = feedback_processor._summarize_plan(plan)
        assert "4 steps" in summary
        assert "research" in summary

    def test_summarize_empty_plan(self, feedback_processor):
        """Test summarization of empty plan."""
        assert "No plan" in feedback_processor._summarize_plan({})
        assert "Empty plan" in feedback_processor._summarize_plan({"steps": []})


class TestInsightExtraction:
    """Test actionable insight extraction."""

    @pytest.mark.asyncio
    async def test_extract_insights_from_preferences(self, feedback_processor, mock_db_adapter):
        """Test extracting insights from preference updates."""
        mock_db_adapter.db.user_feedback.find.return_value.sort.return_value.limit.return_value.to_list = AsyncMock(
            return_value=[]
        )

        feedback = UserFeedback(
            feedback_id="fb_123",
            task_id="task_123",
            user_id="user_123",
            rating=5,
            sentiment="positive",
            categories=["quality"]
        )

        preference_updates = [
            PreferenceUpdate(
                field="detail_level",
                old_value="medium",
                new_value="concise",
                confidence=0.8,
                reasoning="User prefers brief responses"
            )
        ]

        insights = await feedback_processor.extract_actionable_insights(
            "user_123",
            feedback,
            preference_updates
        )

        assert len(insights) > 0
        assert any(i.category == "preference" for i in insights)

    @pytest.mark.asyncio
    async def test_extract_speed_insights(self, feedback_processor, mock_db_adapter):
        """Test extracting speed-related insights."""
        mock_db_adapter.db.user_feedback.find.return_value.sort.return_value.limit.return_value.to_list = AsyncMock(
            return_value=[]
        )

        feedback = UserFeedback(
            feedback_id="fb_123",
            task_id="task_123",
            user_id="user_123",
            rating=2,
            sentiment="negative",
            categories=["speed"]
        )

        insights = await feedback_processor.extract_actionable_insights(
            "user_123",
            feedback,
            []
        )

        assert any(i.category == "performance" and "speed" in i.insight.lower() for i in insights)

    @pytest.mark.asyncio
    async def test_extract_accuracy_insights(self, feedback_processor, mock_db_adapter):
        """Test extracting accuracy-related insights."""
        mock_db_adapter.db.user_feedback.find.return_value.sort.return_value.limit.return_value.to_list = AsyncMock(
            return_value=[]
        )

        feedback = UserFeedback(
            feedback_id="fb_123",
            task_id="task_123",
            user_id="user_123",
            rating=1,
            sentiment="negative",
            categories=["accuracy"]
        )

        insights = await feedback_processor.extract_actionable_insights(
            "user_123",
            feedback,
            []
        )

        assert any(i.category == "quality" and "accuracy" in i.insight.lower() for i in insights)


class TestPatternAnalysis:
    """Test recurring pattern analysis."""

    @pytest.mark.asyncio
    async def test_analyze_recurring_patterns(self, feedback_processor):
        """Test detection of recurring patterns."""
        recent_feedback = [
            {"categories": ["speed"], "sentiment": "negative"},
            {"categories": ["speed"], "sentiment": "negative"},
            {"categories": ["speed"], "sentiment": "negative"},
            {"categories": ["quality"], "sentiment": "positive"}
        ]

        insights = await feedback_processor._analyze_feedback_patterns(recent_feedback)

        # Should detect recurring speed issue
        assert len(insights) > 0
        assert any("speed" in i.insight.lower() for i in insights)

    @pytest.mark.asyncio
    async def test_no_recurring_patterns(self, feedback_processor):
        """Test when no recurring patterns exist."""
        recent_feedback = [
            {"categories": ["speed"], "sentiment": "negative"},
            {"categories": ["quality"], "sentiment": "positive"}
        ]

        insights = await feedback_processor._analyze_feedback_patterns(recent_feedback)

        # Should not detect patterns with only 1-2 occurrences
        assert len(insights) == 0


class TestFullProcessingPipeline:
    """Test complete feedback processing pipeline."""

    @pytest.mark.asyncio
    async def test_process_feedback_complete(self, feedback_processor, mock_db_adapter):
        """Test complete feedback processing pipeline."""
        # Setup mocks
        task_doc = {
            "task_id": "task_123",
            "goal": {"request": "Test task"},
            "plan": {"steps": [{"action": "test"}]},
            "status": "COMPLETED",
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        }

        mock_db_adapter.tasks.find_one = AsyncMock(return_value=task_doc)
        mock_db_adapter.traces.find.return_value.sort.return_value.to_list = AsyncMock(return_value=[])
        mock_db_adapter.decisions.find.return_value.sort.return_value.to_list = AsyncMock(return_value=[])
        mock_db_adapter.db.user_profiles.find_one = AsyncMock(return_value=None)
        mock_db_adapter.db.user_profiles.update_one = AsyncMock()
        mock_db_adapter.db.historical_patterns.insert_one = AsyncMock()
        mock_db_adapter.db.user_feedback.insert_one = AsyncMock()
        mock_db_adapter.db.user_feedback.find.return_value.sort.return_value.limit.return_value.to_list = AsyncMock(
            return_value=[]
        )

        result = await feedback_processor.process_feedback(
            task_id="task_123",
            user_id="user_123",
            rating=5,
            text_feedback="Great job, very thorough!"
        )

        assert "feedback_id" in result
        assert result["sentiment"] == "positive"
        assert "correlations" in result
        assert "insights" in result
        assert "recommendations_for_future" in result

    @pytest.mark.asyncio
    async def test_process_feedback_error_handling(self, feedback_processor, mock_db_adapter):
        """Test error handling in feedback processing."""
        # Setup mocks to succeed initially but force error on creating feedback object
        # This will trigger the exception handler in process_feedback

        # Mock the database operations that should fail early
        with patch('src.memory.learning.feedback_processor.shortuuid') as mock_uuid:
            mock_uuid.uuid.side_effect = Exception("UUID generation error")

            result = await feedback_processor.process_feedback(
                task_id="task_123",
                user_id="user_123",
                rating=5,
                text_feedback=None
            )

            assert "error" in result


class TestDatabaseOperations:
    """Test database operations."""

    @pytest.mark.asyncio
    async def test_save_feedback(self, feedback_processor, mock_db_adapter):
        """Test saving feedback to database."""
        feedback = UserFeedback(
            feedback_id="fb_123",
            task_id="task_123",
            user_id="user_123",
            rating=5,
            sentiment="positive"
        )

        mock_db_adapter.db.user_feedback.insert_one = AsyncMock()

        result = await feedback_processor.save_feedback(feedback)

        assert result is True
        mock_db_adapter.db.user_feedback.insert_one.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_user_preferences(self, feedback_processor, mock_db_adapter):
        """Test retrieving user preferences."""
        user_doc = {
            "user_id": "user_123",
            "preferences": {
                "document_tone": "professional",
                "detail_level": "medium",
                "preferred_formats": ["markdown"],
                "formatting_rules": {}
            }
        }

        mock_db_adapter.db.user_profiles.find_one = AsyncMock(return_value=user_doc)

        prefs = await feedback_processor.get_user_preferences("user_123")

        assert prefs is not None
        assert prefs.document_tone == "professional"
        assert prefs.detail_level == "medium"

    @pytest.mark.asyncio
    async def test_get_recent_feedback(self, feedback_processor, mock_db_adapter):
        """Test retrieving recent feedback."""
        feedback_list = [
            {"feedback_id": "fb_1", "rating": 5},
            {"feedback_id": "fb_2", "rating": 4}
        ]

        # Create a proper async mock chain
        mock_cursor = AsyncMock()
        mock_cursor.to_list = AsyncMock(return_value=feedback_list)

        mock_limit = MagicMock(return_value=mock_cursor)
        mock_sort = MagicMock(return_value=MagicMock(limit=mock_limit))
        mock_db_adapter.db.user_feedback.find = MagicMock(return_value=MagicMock(sort=mock_sort))

        result = await feedback_processor.get_recent_feedback("user_123", limit=10)

        assert len(result) == 2
        assert result[0]["feedback_id"] == "fb_1"

    @pytest.mark.asyncio
    async def test_get_feedback_stats(self, feedback_processor, mock_db_adapter):
        """Test getting feedback statistics."""
        stats = {
            "_id": None,
            "avg_rating": 4.5,
            "total_feedback": 10,
            "positive_count": 7,
            "negative_count": 1
        }

        # Create a proper async mock for aggregate
        mock_aggregate_result = AsyncMock()
        mock_aggregate_result.to_list = AsyncMock(return_value=[stats])

        mock_db_adapter.db.user_feedback.aggregate = MagicMock(return_value=mock_aggregate_result)

        result = await feedback_processor.get_feedback_stats("user_123")

        assert result["avg_rating"] == 4.5
        assert result["total_feedback"] == 10


class TestRecommendationGeneration:
    """Test recommendation generation."""

    @pytest.mark.asyncio
    async def test_generate_recommendations_high_confidence(self, feedback_processor):
        """Test generating recommendations from high-confidence insights."""
        insights = [
            FeedbackInsight(
                insight="User prefers concise",
                confidence=0.9,
                action="Set detail_level to concise",
                category="preference"
            ),
            FeedbackInsight(
                insight="Quality issue",
                confidence=0.85,
                action="Increase validation",
                category="quality"
            )
        ]

        recommendations = await feedback_processor._generate_recommendations(insights)

        assert len(recommendations) > 0
        assert "Set detail_level to concise" in recommendations
        assert "Increase validation" in recommendations

    @pytest.mark.asyncio
    async def test_generate_recommendations_category_based(self, feedback_processor):
        """Test category-based recommendations."""
        insights = [
            FeedbackInsight(
                insight="Test",
                confidence=0.9,
                action="Test action",
                category="preference"
            )
        ]

        recommendations = await feedback_processor._generate_recommendations(insights)

        assert any("preferences" in r.lower() for r in recommendations)
