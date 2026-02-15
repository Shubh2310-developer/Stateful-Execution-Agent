"""
Example: Using the FeedbackProcessor

This example demonstrates how to use the FeedbackProcessor to process user feedback
and update long-term memory, preferences, and historical patterns.
"""

import asyncio
from datetime import datetime, timezone

from src.memory.learning.feedback_processor import FeedbackProcessor
from src.state.persistence.database_adapter import DatabaseAdapter


async def example_basic_feedback_processing():
    """Example 1: Basic feedback processing with rating only."""

    print("=" * 80)
    print("Example 1: Basic Feedback Processing")
    print("=" * 80)

    # Initialize processor
    db_adapter = DatabaseAdapter()
    processor = FeedbackProcessor(db_adapter=db_adapter)

    # Process simple rating feedback
    result = await processor.process_feedback(
        task_id="task_example_001",
        user_id="user_example_001",
        rating=5,
        text_feedback=None
    )

    print(f"\nFeedback ID: {result.get('feedback_id')}")
    print(f"Sentiment: {result.get('sentiment')}")
    print(f"Historical Pattern Updated: {result.get('historical_pattern_updated')}")

    db_adapter.client.close()


async def example_detailed_feedback_with_text():
    """Example 2: Detailed feedback with text analysis."""

    print("\n" + "=" * 80)
    print("Example 2: Detailed Feedback with Text Analysis")
    print("=" * 80)

    db_adapter = DatabaseAdapter()
    processor = FeedbackProcessor(db_adapter=db_adapter)

    # Process detailed feedback with text
    result = await processor.process_feedback(
        task_id="task_example_002",
        user_id="user_example_002",
        rating=4,
        text_feedback="Great analysis, but the report was too verbose. I prefer concise summaries with bullet points. Also, please include more citations next time."
    )

    print(f"\nFeedback ID: {result.get('feedback_id')}")
    print(f"Sentiment: {result.get('sentiment')}")
    print(f"\nCategories Detected: {result.get('categories')}")

    print(f"\nPreference Updates ({len(result.get('preference_updates', []))}):")
    for update in result.get('preference_updates', []):
        print(f"  - {update['field']}: {update['old_value']} -> {update['new_value']}")
        print(f"    Confidence: {update['confidence']:.2f}")
        print(f"    Reasoning: {update['reasoning']}")

    print(f"\nInsights ({len(result.get('insights', []))}):")
    for insight in result.get('insights', []):
        print(f"  - {insight['insight']}")
        print(f"    Action: {insight['action']}")
        print(f"    Confidence: {insight['confidence']:.2f}")

    print(f"\nRecommendations for Future:")
    for rec in result.get('recommendations_for_future', []):
        print(f"  - {rec}")

    db_adapter.client.close()


async def example_negative_feedback_correlation():
    """Example 3: Negative feedback with execution correlation."""

    print("\n" + "=" * 80)
    print("Example 3: Negative Feedback with Execution Correlation")
    print("=" * 80)

    db_adapter = DatabaseAdapter()
    processor = FeedbackProcessor(db_adapter=db_adapter)

    # First, create some execution trace data
    task_id = "task_example_003"
    user_id = "user_example_003"

    # Simulate task execution traces
    await db_adapter.traces.insert_many([
        {
            "task_id": task_id,
            "step_id": "step_research",
            "event_type": "execution",
            "timestamp": datetime.now(timezone.utc),
            "action_taken": {"action": "web_search"},
            "outcome": {"status": "success", "sources_found": 5}
        },
        {
            "task_id": task_id,
            "step_id": "step_analysis",
            "event_type": "execution",
            "timestamp": datetime.now(timezone.utc),
            "action_taken": {"action": "analyze_data"},
            "outcome": {"status": "success"}
        }
    ])

    # Simulate decision logs
    await db_adapter.decisions.insert_many([
        {
            "decision_id": "dec_source_selection",
            "task_id": task_id,
            "step_id": "step_research",
            "timestamp": datetime.now(timezone.utc),
            "decision_point": "Choose research sources",
            "final_choice": "Wikipedia and blogs",
            "confidence_score": 0.45  # Low confidence
        }
    ])

    # Process negative feedback
    result = await processor.process_feedback(
        task_id=task_id,
        user_id=user_id,
        rating=2,
        text_feedback="The research sources were not credible. I need academic sources, not Wikipedia."
    )

    print(f"\nFeedback ID: {result.get('feedback_id')}")
    print(f"Sentiment: {result.get('sentiment')}")

    print(f"\nCorrelations to Execution:")
    correlations = result.get('correlations', {})
    if correlations.get('steps'):
        print("  Steps:")
        for step_id, score in correlations['steps'].items():
            print(f"    - {step_id}: {score:.2f}")

    if correlations.get('decisions'):
        print("  Decisions:")
        for dec_id, score in correlations['decisions'].items():
            print(f"    - {dec_id}: {score:.2f}")

    print(f"\nInsights:")
    for insight in result.get('insights', []):
        print(f"  - {insight['insight']}")
        print(f"    Category: {insight['category']}")

    # Cleanup
    await db_adapter.traces.delete_many({"task_id": task_id})
    await db_adapter.decisions.delete_many({"task_id": task_id})
    db_adapter.client.close()


async def example_recurring_pattern_detection():
    """Example 4: Detecting recurring patterns across multiple feedback items."""

    print("\n" + "=" * 80)
    print("Example 4: Recurring Pattern Detection")
    print("=" * 80)

    db_adapter = DatabaseAdapter()
    processor = FeedbackProcessor(db_adapter=db_adapter)

    user_id = "user_example_004"

    # Simulate multiple tasks with similar feedback
    print("\nSubmitting feedback for 5 tasks with recurring speed complaints...")

    for i in range(5):
        task_id = f"task_speed_{i}"

        # Create task
        await db_adapter.tasks.insert_one({
            "task_id": task_id,
            "user_id": user_id,
            "goal": {"request": f"Analysis task {i}"},
            "plan": {"steps": [{"action": "analyze"}]},
            "status": "COMPLETED",
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        })

        # Submit feedback
        await processor.process_feedback(
            task_id=task_id,
            user_id=user_id,
            rating=2,
            text_feedback="The task took too long to complete. Please optimize for speed."
        )

    # Get recent feedback to analyze patterns
    recent_feedback = await processor.get_recent_feedback(user_id, limit=10)

    print(f"\nTotal feedback items: {len(recent_feedback)}")

    # Process one more feedback and check for pattern detection
    result = await processor.process_feedback(
        task_id="task_speed_final",
        user_id=user_id,
        rating=2,
        text_feedback="Again, performance was too slow."
    )

    print(f"\nDetected Insights:")
    for insight in result.get('insights', []):
        if insight['category'] == 'recurring_pattern':
            print(f"  - RECURRING: {insight['insight']}")
            print(f"    Confidence: {insight['confidence']:.2f}")
            print(f"    Recommended Action: {insight['action']}")

    # Cleanup
    for i in range(5):
        await db_adapter.tasks.delete_one({"task_id": f"task_speed_{i}"})
    db_adapter.client.close()


async def example_feedback_statistics():
    """Example 5: Aggregating feedback statistics."""

    print("\n" + "=" * 80)
    print("Example 5: Feedback Statistics")
    print("=" * 80)

    db_adapter = DatabaseAdapter()
    processor = FeedbackProcessor(db_adapter=db_adapter)

    user_id = "user_example_005"

    # Submit various ratings
    print("\nSubmitting 10 feedback items with various ratings...")

    ratings = [5, 5, 4, 4, 4, 3, 3, 2, 2, 1]

    for i, rating in enumerate(ratings):
        task_id = f"task_stats_{i}"

        await db_adapter.tasks.insert_one({
            "task_id": task_id,
            "user_id": user_id,
            "goal": {"request": f"Task {i}"},
            "plan": {"steps": [{"action": "test"}]},
            "status": "COMPLETED",
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        })

        await processor.process_feedback(
            task_id=task_id,
            user_id=user_id,
            rating=rating,
            text_feedback=f"Rating {rating} feedback"
        )

    # Get statistics
    stats = await processor.get_feedback_stats(user_id)

    print(f"\nFeedback Statistics for {user_id}:")
    print(f"  Total Feedback: {stats.get('total_feedback', 0)}")
    print(f"  Average Rating: {stats.get('avg_rating', 0):.2f}")
    print(f"  Positive Feedback (4-5): {stats.get('positive_count', 0)}")
    print(f"  Negative Feedback (1-2): {stats.get('negative_count', 0)}")

    # Cleanup
    for i in range(10):
        await db_adapter.tasks.delete_one({"task_id": f"task_stats_{i}"})
    db_adapter.client.close()


async def example_preference_persistence():
    """Example 6: Demonstrating preference persistence across sessions."""

    print("\n" + "=" * 80)
    print("Example 6: Preference Persistence")
    print("=" * 80)

    db_adapter = DatabaseAdapter()
    processor = FeedbackProcessor(db_adapter=db_adapter)

    user_id = "user_example_006"

    # First feedback session
    print("\nSession 1: User provides feedback about verbosity...")

    await db_adapter.tasks.insert_one({
        "task_id": "task_prefs_1",
        "user_id": user_id,
        "goal": {"request": "Report generation"},
        "plan": {"steps": [{"action": "generate"}]},
        "status": "COMPLETED",
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc)
    })

    result1 = await processor.process_feedback(
        task_id="task_prefs_1",
        user_id=user_id,
        rating=3,
        text_feedback="Too verbose, please be more concise"
    )

    print(f"Preference updates: {len(result1.get('preference_updates', []))}")

    # Retrieve stored preferences
    print("\nRetrieving stored preferences...")
    prefs = await processor.get_user_preferences(user_id)

    if prefs:
        print(f"  Detail Level: {prefs.detail_level}")
        print(f"  Document Tone: {prefs.document_tone}")
        print(f"  Preferred Formats: {prefs.preferred_formats}")
    else:
        print("  No preferences found (will use defaults)")

    # Second feedback session (different preference)
    print("\nSession 2: User provides feedback about tone...")

    await db_adapter.tasks.insert_one({
        "task_id": "task_prefs_2",
        "user_id": user_id,
        "goal": {"request": "Analysis report"},
        "plan": {"steps": [{"action": "analyze"}]},
        "status": "COMPLETED",
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc)
    })

    result2 = await processor.process_feedback(
        task_id="task_prefs_2",
        user_id=user_id,
        rating=4,
        text_feedback="Good work, but please use a more professional tone"
    )

    print(f"Preference updates: {len(result2.get('preference_updates', []))}")

    # Retrieve updated preferences
    print("\nRetrieving updated preferences...")
    prefs_updated = await processor.get_user_preferences(user_id)

    if prefs_updated:
        print(f"  Detail Level: {prefs_updated.detail_level}")
        print(f"  Document Tone: {prefs_updated.document_tone}")
        print(f"  Preferred Formats: {prefs_updated.preferred_formats}")

    # Cleanup
    await db_adapter.tasks.delete_one({"task_id": "task_prefs_1"})
    await db_adapter.tasks.delete_one({"task_id": "task_prefs_2"})
    db_adapter.client.close()


async def main():
    """Run all examples."""

    print("\n" + "=" * 80)
    print("FeedbackProcessor Examples")
    print("=" * 80)

    # Note: These examples require MongoDB to be running
    # You can uncomment the examples you want to run

    # await example_basic_feedback_processing()
    # await example_detailed_feedback_with_text()
    # await example_negative_feedback_correlation()
    # await example_recurring_pattern_detection()
    # await example_feedback_statistics()
    # await example_preference_persistence()

    print("\n" + "=" * 80)
    print("Examples completed!")
    print("=" * 80)
    print("\nNote: Uncomment the example functions in main() to run them.")
    print("Ensure MongoDB is running before executing these examples.")


if __name__ == "__main__":
    asyncio.run(main())
