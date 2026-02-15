import pytest
import asyncio
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch
from src.reviewer.reviewer import Reviewer
from src.reviewer.quality_checker import QualityChecker
from src.core.types import (
    TaskState, Goal, Plan, Step, Artifact, TaskStatus
)


@pytest.fixture
def sample_task_state():
    """Creates a sample task state for testing."""
    goal = Goal(
        request="Create a comprehensive market analysis report for Q4 2025",
        success_criteria=[
            "Report must include at least 3 market segments",
            "Data must be from Q4 2025",
            "Analysis must include recommendations",
            "Format must be professional PDF"
        ],
        constraints=["Maximum 10 pages", "Professional tone"]
    )

    step1 = Step(
        step_id="step_001",
        order=1,
        action="gather_market_data",
        description="Gather market data for Q4 2025",
        success_criteria="Data collected for at least 3 segments",
        status=TaskStatus.COMPLETED
    )

    step2 = Step(
        step_id="step_002",
        order=2,
        action="analyze_data",
        description="Analyze collected market data",
        success_criteria="Analysis includes trends and insights",
        status=TaskStatus.COMPLETED
    )

    step3 = Step(
        step_id="step_003",
        order=3,
        action="generate_report",
        description="Generate final report document",
        success_criteria="Report is in PDF format with all sections",
        status=TaskStatus.COMPLETED
    )

    plan = Plan(
        task_id="task_123",
        steps=[step1, step2, step3]
    )

    artifact1 = Artifact(
        id="art_001",
        task_id="task_123",
        step_id="step_001",
        uri="file:///tmp/market_data.json",
        type="data",
        size_bytes=15000
    )

    artifact2 = Artifact(
        id="art_002",
        task_id="task_123",
        step_id="step_002",
        uri="file:///tmp/analysis.json",
        type="data",
        size_bytes=8000
    )

    artifact3 = Artifact(
        id="art_003",
        task_id="task_123",
        step_id="step_003",
        uri="file:///tmp/report.pdf",
        type="document",
        mime_type="application/pdf",
        size_bytes=250000
    )

    state = TaskState(
        task_id="task_123",
        user_id="user_456",
        goal=goal,
        plan=plan,
        artifacts=[artifact1, artifact2, artifact3],
        status=TaskStatus.COMPLETED,
        current_step_index=3
    )

    return state


@pytest.fixture
def mock_artifact_manager():
    """Mocks the ArtifactManager."""
    manager = MagicMock()
    manager.get_artifact_content = MagicMock(side_effect=lambda art: {
        "art_001": {"segments": ["retail", "technology", "healthcare"], "period": "Q4 2025"},
        "art_002": {"trends": ["growth in tech", "retail decline"], "insights": "Market volatility high"},
        "art_003": "# Market Analysis Report Q4 2025\n\n## Executive Summary\n..."
    }.get(art.id, ""))
    return manager


@pytest.fixture
def mock_groq_client():
    """Mocks the Groq LLM client."""
    with patch('src.reviewer.reviewer.groq_client') as mock_client:
        # Default successful review response
        mock_client.generate_response = AsyncMock(return_value='''{
            "reasoning": "Comprehensive review completed. All success criteria evaluated.",
            "overall_success": true,
            "needs_revision": false,
            "quality_score": 85,
            "requirement_coverage": {
                "total_requirements": 4,
                "met_requirements": 4,
                "partially_met": 0,
                "unmet_requirements": 0,
                "coverage_percentage": 100
            },
            "success_criteria_status": [
                {"criterion": "Report must include at least 3 market segments", "status": "MET", "evidence": "Found 3 segments in data"},
                {"criterion": "Data must be from Q4 2025", "status": "MET", "evidence": "Period confirmed in artifact"},
                {"criterion": "Analysis must include recommendations", "status": "MET", "evidence": "Insights present"},
                {"criterion": "Format must be professional PDF", "status": "MET", "evidence": "PDF artifact produced"}
            ],
            "artifact_assessment": [
                {"artifact_id": "art_001", "artifact_type": "data", "status": "COMPLETE", "quality_notes": "Good data structure"},
                {"artifact_id": "art_002", "artifact_type": "data", "status": "COMPLETE", "quality_notes": "Solid analysis"},
                {"artifact_id": "art_003", "artifact_type": "document", "status": "COMPLETE", "quality_notes": "Professional format"}
            ],
            "strengths": ["Comprehensive data collection", "Clear analysis", "Professional formatting"],
            "weaknesses": [],
            "revision_instructions": [],
            "feedback": "Excellent work. All requirements met.",
            "recommendations": ["Consider adding executive summary"]
        }''')
        yield mock_client


@pytest.mark.asyncio
class TestReviewer:
    """Tests for the Reviewer class."""

    async def test_review_task_success(self, sample_task_state, mock_artifact_manager, mock_groq_client):
        """Test successful review without revision needed."""
        reviewer = Reviewer(max_iterations=2)
        reviewer.artifact_manager = mock_artifact_manager

        # Mock quality checker
        with patch.object(reviewer.quality_checker, 'check_quality', new_callable=AsyncMock) as mock_quality:
            mock_quality.return_value = {
                "quality_score": 85.0,
                "passed": True,
                "static_score": 90.0,
                "llm_score": 82.0,
                "static_checks": {"file_exists": True, "content_not_empty": True},
                "llm_checks": {"tone_consistency": True},
                "strengths": ["Well structured"],
                "weaknesses": [],
                "recommendations": []
            }

            result = await reviewer.review_task(sample_task_state)

            assert result["task_id"] == "task_123"
            assert result["overall_success"] is True
            assert result["needs_revision"] is False
            assert result["quality_score"] > 70.0
            assert result["iteration_count"] == 0
            assert len(result["revision_instructions"]) == 0

    async def test_review_task_needs_revision(self, sample_task_state, mock_artifact_manager):
        """Test review that identifies need for revision."""
        reviewer = Reviewer(max_iterations=2)
        reviewer.artifact_manager = mock_artifact_manager

        # Mock LLM to return needs_revision=True
        with patch('src.reviewer.reviewer.groq_client') as mock_client:
            mock_client.generate_response = AsyncMock(return_value='''{
                "reasoning": "Report missing key requirements",
                "overall_success": false,
                "needs_revision": true,
                "quality_score": 55,
                "requirement_coverage": {
                    "total_requirements": 4,
                    "met_requirements": 2,
                    "partially_met": 1,
                    "unmet_requirements": 1,
                    "coverage_percentage": 50
                },
                "success_criteria_status": [
                    {"criterion": "Report must include at least 3 market segments", "status": "MET", "evidence": "Found 3 segments"},
                    {"criterion": "Data must be from Q4 2025", "status": "NOT_MET", "evidence": "No date verification"},
                    {"criterion": "Analysis must include recommendations", "status": "PARTIALLY_MET", "evidence": "Weak recommendations"},
                    {"criterion": "Format must be professional PDF", "status": "MET", "evidence": "PDF present"}
                ],
                "artifact_assessment": [],
                "strengths": ["Good data structure"],
                "weaknesses": ["Missing date verification", "Weak recommendations"],
                "revision_instructions": [
                    "Add explicit Q4 2025 date verification in data section",
                    "Strengthen recommendations with specific action items"
                ],
                "feedback": "Report needs revision to meet quality standards",
                "recommendations": []
            }''')

            # Mock quality checker
            with patch.object(reviewer.quality_checker, 'check_quality', new_callable=AsyncMock) as mock_quality:
                mock_quality.return_value = {
                    "quality_score": 60.0,
                    "passed": False,
                    "static_checks": {},
                    "llm_checks": {}
                }

                result = await reviewer.review_task(sample_task_state)

                assert result["overall_success"] is False
                assert result["needs_revision"] is True
                assert result["quality_score"] < 70.0
                assert len(result["revision_instructions"]) == 2
                assert "Q4 2025 date verification" in result["revision_instructions"][0]

    async def test_quality_score_calculation(self, sample_task_state, mock_artifact_manager, mock_groq_client):
        """Test quality score calculation combining LLM and artifact scores."""
        reviewer = Reviewer(max_iterations=2)
        reviewer.artifact_manager = mock_artifact_manager

        # Mock quality checker with specific scores
        with patch.object(reviewer.quality_checker, 'check_quality', new_callable=AsyncMock) as mock_quality:
            mock_quality.return_value = {
                "quality_score": 80.0,
                "static_checks": {},
                "llm_checks": {}
            }

            result = await reviewer.review_task(sample_task_state)

            # Should combine LLM score (85) at 60% and artifact scores (80) at 40%
            # Expected: 85 * 0.6 + 80 * 0.4 = 51 + 32 = 83
            assert "quality_score" in result
            assert isinstance(result["quality_score"], float)

    async def test_max_iterations_enforcement(self, sample_task_state, mock_artifact_manager):
        """Test that max_iterations limit is enforced."""
        reviewer = Reviewer(max_iterations=2)
        reviewer.artifact_manager = mock_artifact_manager

        # Mock always needs revision
        with patch('src.reviewer.reviewer.groq_client') as mock_client:
            mock_client.generate_response = AsyncMock(return_value='''{
                "reasoning": "Always needs work",
                "overall_success": false,
                "needs_revision": true,
                "quality_score": 50,
                "revision_instructions": ["Fix everything"],
                "feedback": "Not good enough"
            }''')

            with patch.object(reviewer.quality_checker, 'check_quality', new_callable=AsyncMock) as mock_quality:
                mock_quality.return_value = {"quality_score": 50.0, "static_checks": {}, "llm_checks": {}}

                # Test single review
                result = await reviewer.review_task(sample_task_state, iteration_count=0)
                assert result["needs_revision"] is True

                # Test at max iteration
                result = await reviewer.review_task(sample_task_state, iteration_count=2)
                assert result["needs_revision"] is False  # Should not allow further revision


@pytest.mark.asyncio
class TestQualityChecker:
    """Tests for the QualityChecker class."""

    async def test_static_checks_valid_artifact(self):
        """Test static checks on valid artifact."""
        checker = QualityChecker()

        artifact = Artifact(
            id="test_001",
            task_id="task_123",
            uri="file:///tmp/test.json",
            type="data",
            size_bytes=1000
        )

        content = {"key": "value", "data": [1, 2, 3]}

        result = await checker._run_static_checks(artifact, content)

        assert result["score"] > 0
        assert result["passed_count"] > 0
        assert result["checks"]["content_not_empty"] is True
        assert result["checks"]["size_reasonable"] is True

    async def test_static_checks_empty_content(self):
        """Test static checks fail on empty content."""
        checker = QualityChecker()

        artifact = Artifact(
            id="test_002",
            task_id="task_123",
            uri="file:///tmp/empty.json",
            type="data",
            size_bytes=0
        )

        content = ""

        result = await checker._run_static_checks(artifact, content)

        assert result["checks"]["content_not_empty"] is False
        assert len(result["issues"]) > 0
        assert any("empty" in issue.lower() for issue in result["issues"])

    async def test_quality_score_calculation(self):
        """Test weighted quality score calculation."""
        checker = QualityChecker()

        static_score = 80.0
        llm_score = 90.0

        combined = checker._calculate_quality_score(static_score, llm_score)

        # Expected: 80 * 0.4 + 90 * 0.6 = 32 + 54 = 86
        assert combined == 86.0

    async def test_quality_level_labels(self):
        """Test quality level label assignment."""
        checker = QualityChecker()

        assert checker._get_quality_level(95) == "EXCELLENT"
        assert checker._get_quality_level(85) == "GOOD"
        assert checker._get_quality_level(75) == "ACCEPTABLE"
        assert checker._get_quality_level(60) == "MARGINAL"
        assert checker._get_quality_level(40) == "POOR"

    async def test_format_validation_json(self):
        """Test JSON format validation."""
        checker = QualityChecker()

        artifact = Artifact(
            id="test_003",
            task_id="task_123",
            uri="file:///tmp/data.json",
            type="data",
            mime_type="application/json"
        )

        # Valid JSON
        valid_content = {"test": "data"}
        result = checker._check_format_validity(artifact, valid_content)
        assert result["valid"] is True

        # Invalid JSON string
        invalid_content = "{invalid json"
        result = checker._check_format_validity(artifact, invalid_content)
        assert result["valid"] is False
        assert "error" in result

    async def test_structure_validation(self):
        """Test structure validation for different types."""
        checker = QualityChecker()

        # Data artifact - should be dict or list
        data_artifact = Artifact(
            id="test_004",
            task_id="task_123",
            uri="file:///tmp/data.json",
            type="data"
        )

        valid_data = {"key": "value"}
        result = checker._check_structure(data_artifact, valid_data)
        assert result["valid"] is True

        invalid_data = "just a string"
        result = checker._check_structure(data_artifact, invalid_data)
        assert result["valid"] is False

        # Document artifact - should be non-empty string
        doc_artifact = Artifact(
            id="test_005",
            task_id="task_123",
            uri="file:///tmp/doc.txt",
            type="document"
        )

        valid_doc = "This is a document with content"
        result = checker._check_structure(doc_artifact, valid_doc)
        assert result["valid"] is True


@pytest.mark.asyncio
class TestReviewIteration:
    """Tests for review iteration and correction loop."""

    async def test_review_with_correction_loop_success_first_try(
        self, sample_task_state, mock_artifact_manager, mock_groq_client
    ):
        """Test correction loop when task passes on first review."""
        reviewer = Reviewer(max_iterations=2)
        reviewer.artifact_manager = mock_artifact_manager

        with patch.object(reviewer.quality_checker, 'check_quality', new_callable=AsyncMock) as mock_quality:
            mock_quality.return_value = {
                "quality_score": 85.0,
                "static_checks": {},
                "llm_checks": {}
            }

            result = await reviewer.review_with_correction_loop(sample_task_state)

            assert result["overall_success"] is True
            assert result["iteration_count"] == 0
            assert result["needs_revision"] is False

    async def test_iteration_count_tracking(self, sample_task_state, mock_artifact_manager):
        """Test that iteration count is properly tracked."""
        reviewer = Reviewer(max_iterations=2)
        reviewer.artifact_manager = mock_artifact_manager

        with patch.object(reviewer.quality_checker, 'check_quality', new_callable=AsyncMock) as mock_quality:
            mock_quality.return_value = {"quality_score": 85.0, "static_checks": {}, "llm_checks": {}}

            # Review at different iterations
            result_0 = await reviewer.review_task(sample_task_state, iteration_count=0)
            assert result_0["iteration_count"] == 0

            result_1 = await reviewer.review_task(sample_task_state, iteration_count=1)
            assert result_1["iteration_count"] == 1

            result_2 = await reviewer.review_task(sample_task_state, iteration_count=2)
            assert result_2["iteration_count"] == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
