"""
Integration test for FeedbackProcessor.

This test demonstrates the full feedback processing pipeline with a real database.
Note: Requires MongoDB to be running and configured.
"""

import pytest
import asyncio
from datetime import datetime, UTC

from src.memory.learning.feedback_processor import FeedbackProcessor
from src.state.persistence.database_adapter import DatabaseAdapter
from src.core.config import settings


@pytest.fixture(scope="function")
async def test_db_adapter():
    """Create a test database adapter with a separate test database."""
    adapter = DatabaseAdapter()
    # Use a test database
    adapter.db = adapter.client["agent_state_test_integration"]

    yield adapter

    # Cleanup after tests
    try:
        await adapter.client.drop_database("agent_state_test_integration")
    except Exception:
        pass
    adapter.client.close()


@pytest.fixture(scope="function")
async def feedback_processor_integration(test_db_adapter):
    """Create a FeedbackProcessor with real database."""
    return FeedbackProcessor(db_adapter=test_db_adapter)


@pytest.mark.asyncio
async def test_full_feedback_pipeline_integration(
    feedback_processor_integration,
    test_db_adapter
):
    """Test the complete feedback processing pipeline with real database operations."""

    # Setup: Create a test task
    task_doc = {
        "task_id": "task_integration_123",
        "user_id": "user_integration_123",
        "goal": {
            "request": "Generate a comprehensive market analysis report",
            "success_criteria": ["Include data", "Citations required"]
        },
        "plan": {
            "steps": [
                {"step_id": "step_1", "action": "research", "description": "Research market data", "status": "COMPLETED"},
                {"step_id": "step_2", "action": "analyze", "description": "Analyze trends", "status": "COMPLETED"},
                {"step_id": "step_3", "action": "write", "description": "Write report", "status": "COMPLETED"}
            ]
        },
        "status": "COMPLETED",
        "created_at": datetime.now(UTC),
        "updated_at": datetime.now(UTC),
        "metadata": {}
    }

    await test_db_adapter.tasks.insert_one(task_doc)

    # Create some trace data
    traces = [
        {
            "task_id": "task_integration_123",
            "step_id": "step_1",
            "event_type": "execution",
            "timestamp": datetime.now(UTC),
            "action_taken": {"action": "research"},
            "outcome": {"status": "success"}
        },
        {
            "task_id": "task_integration_123",
            "step_id": "step_2",
            "event_type": "execution",
            "timestamp": datetime.now(UTC),
            "action_taken": {"action": "analyze"},
            "outcome": {"status": "success"}
        }
    ]

    await test_db_adapter.traces.insert_many(traces)

    # Create some decision data
    decisions = [
        {
            "decision_id": "dec_1",
            "task_id": "task_integration_123",
            "step_id": "step_1",
            "timestamp": datetime.now(UTC),
            "decision_point": "Choose research sources",
            "final_choice": "Academic journals",
            "confidence_score": 0.9
        }
    ]

    await test_db_adapter.decisions.insert_many(decisions)

    # Process feedback
    result = await feedback_processor_integration.process_feedback(
        task_id="task_integration_123",
        user_id="user_integration_123",
        rating=4,
        text_feedback="Good work, but the report was too verbose. I prefer concise summaries."
    )

    # Assertions
    assert "feedback_id" in result
    assert result["sentiment"] == "positive"
    assert len(result["categories"]) > 0
    assert result["historical_pattern_updated"] is True

    # Check that preferences were updated
    assert len(result["preference_updates"]) > 0
    detail_level_update = next(
        (u for u in result["preference_updates"] if u["field"] == "detail_level"),
        None
    )
    assert detail_level_update is not None
    assert detail_level_update.new_value == "concise"

    # Check insights were generated
    assert len(result["insights"]) > 0

    # Check recommendations were generated
    assert len(result["recommendations_for_future"]) > 0

    # Verify data was saved to database
    saved_feedback = await test_db_adapter.db.user_feedback.find_one(
        {"feedback_id": result["feedback_id"]}
    )
    assert saved_feedback is not None
    assert saved_feedback["rating"] == 4

    # Verify historical pattern was created
    pattern = await test_db_adapter.db.historical_patterns.find_one(
        {"task_id": "task_integration_123"}
    )
    assert pattern is not None
    assert pattern["success_score"] == 0.8  # 4/5

    # Verify user preferences were updated
    user_prefs = await test_db_adapter.db.user_profiles.find_one(
        {"user_id": "user_integration_123"}
    )
    assert user_prefs is not None
    assert user_prefs["preferences"]["detail_level"] == "concise"


@pytest.mark.asyncio
async def test_multiple_feedback_pattern_detection(
    feedback_processor_integration,
    test_db_adapter
):
    """Test that recurring patterns are detected across multiple feedback items."""

    # Setup: Create a test task
    for i in range(5):
        task_doc = {
            "task_id": f"task_pattern_{i}",
            "user_id": "user_pattern_test",
            "goal": {"request": f"Test task {i}"},
            "plan": {"steps": [{"action": "test", "status": "COMPLETED"}]},
            "status": "COMPLETED",
            "created_at": datetime.now(UTC),
            "updated_at": datetime.now(UTC)
        }
        await test_db_adapter.tasks.insert_one(task_doc)

    # Submit multiple feedback items with similar complaints
    for i in range(5):
        await feedback_processor_integration.process_feedback(
            task_id=f"task_pattern_{i}",
            user_id="user_pattern_test",
            rating=2 if i < 4 else 5,  # 4 negative, 1 positive
            text_feedback="Too slow" if i < 4 else "Great speed!"
        )

    # Process one more feedback and check for pattern detection
    result = await feedback_processor_integration.process_feedback(
        task_id="task_pattern_4",
        user_id="user_pattern_test",
        rating=2,
        text_feedback="Again, this was too slow"
    )

    # Should detect recurring speed issue
    recurring_insights = [
        i for i in result["insights"]
        if i.category == "recurring_pattern" and "speed" in i.insight.lower()
    ]

    assert len(recurring_insights) > 0


@pytest.mark.asyncio
async def test_feedback_stats_aggregation(
    feedback_processor_integration,
    test_db_adapter
):
    """Test feedback statistics aggregation."""

    # Setup tasks
    for i in range(10):
        task_doc = {
            "task_id": f"task_stats_{i}",
            "user_id": "user_stats_test",
            "goal": {"request": f"Test task {i}"},
            "plan": {"steps": [{"action": "test", "status": "COMPLETED"}]},
            "status": "COMPLETED",
            "created_at": datetime.now(UTC),
            "updated_at": datetime.now(UTC)
        }
        await test_db_adapter.tasks.insert_one(task_doc)

    # Submit varying ratings
    ratings = [5, 5, 4, 4, 4, 3, 3, 2, 2, 1]
    for i, rating in enumerate(ratings):
        await feedback_processor_integration.process_feedback(
            task_id=f"task_stats_{i}",
            user_id="user_stats_test",
            rating=rating,
            text_feedback=None
        )

    # Get stats
    stats = await feedback_processor_integration.get_feedback_stats("user_stats_test")

    assert stats["total_feedback"] == 10
    assert stats["avg_rating"] == pytest.approx(3.3, 0.1)
    assert stats["positive_count"] == 5  # Ratings 4-5
    assert stats["negative_count"] == 3  # Ratings 1-2
