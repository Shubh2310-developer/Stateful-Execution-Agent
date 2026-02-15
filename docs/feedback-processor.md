# FeedbackProcessor Documentation

## Overview

The `FeedbackProcessor` is a comprehensive system for processing user feedback and updating long-term memory in the Stateful Execution Agent. It implements Phase 9.3 requirements by analyzing feedback, extracting preferences, correlating to execution traces, and generating actionable insights.

## Architecture

### Core Components

1. **Feedback Data Models**
   - `UserFeedback`: Comprehensive feedback with rating, text, sentiment, categories, and correlations
   - `PreferenceUpdate`: Tracks changes to user preferences
   - `FeedbackInsight`: Actionable insight with confidence score
   - `FeedbackProcessingResult`: Complete processing pipeline result

2. **Processing Pipeline**
   - Rating parsing and sentiment analysis
   - Text feedback parsing (LLM + heuristic fallback)
   - Execution trace correlation
   - User preference updates
   - Historical pattern updates
   - Insight extraction
   - Recommendation generation

3. **Storage Layer**
   - MongoDB collections: `user_feedback`, `user_profiles`, `historical_patterns`
   - Integration with existing `tasks`, `traces`, `decisions` collections

## Key Features

### 1. Rating Parsing

Maps 1-5 ratings to sentiment:
- 4-5: Positive
- 3: Neutral
- 1-2: Negative

### 2. Text Feedback Analysis

Uses Groq LLM to extract:
- Sentiment aspects (positive/negative)
- Preference signals (detail level, tone, format)
- Quality issues (accuracy, completeness, clarity)
- Categories (speed, accuracy, format, tone, etc.)
- Specific mentions (steps, tools, decisions)

Falls back to heuristic parsing if LLM fails.

### 3. Execution Correlation

Correlates feedback to specific execution steps and decisions:
- Uses LLM for intelligent correlation when text feedback is provided
- Uses heuristic correlation based on sentiment and confidence scores
- Returns relevance scores (0.0-1.0) for each correlation

### 4. Preference Updates

Automatically detects and updates preferences:

**Detail Level:**
- "too verbose", "brief" → concise
- "more detail", "comprehensive" → comprehensive

**Document Tone:**
- "professional", "formal" → professional
- "casual", "informal" → casual

**Format Preferences:**
- Negative feedback about PDF → remove from preferred formats
- Positive feedback → add to preferred formats

**Citations:**
- Mentions of "citation", "source", "reference" → enable citation requirement

### 5. Historical Pattern Storage

Creates `HistoricalPattern` entries with:
- Success score (rating / 5.0)
- Plan summary
- Outcome description
- Feedback categories as tags
- Metadata (duration, status, etc.)

### 6. Insight Extraction

Generates actionable insights with confidence scores:

**Preference Insights:**
- Identified from preference updates
- High confidence (0.8+)

**Category Insights:**
- Speed issues → optimize performance
- Accuracy issues → increase validation
- Completeness issues → ensure thorough coverage

**Recurring Pattern Detection:**
- Analyzes recent feedback (last 10 items)
- Identifies categories appearing 3+ times with negative sentiment
- High confidence based on frequency

### 7. Recommendation Generation

Produces specific recommendations for future tasks:
- Based on high-confidence insights (0.8+)
- Category-based general recommendations
- Actionable and specific

## Usage Examples

### Basic Rating Feedback

```python
from src.memory.learning.feedback_processor import FeedbackProcessor

processor = FeedbackProcessor()

result = await processor.process_feedback(
    task_id="task_123",
    user_id="user_123",
    rating=5,
    text_feedback=None
)
```

### Detailed Text Feedback

```python
result = await processor.process_feedback(
    task_id="task_456",
    user_id="user_123",
    rating=4,
    text_feedback="Great work, but too verbose. Please be more concise next time."
)

# Access results
print(f"Sentiment: {result['sentiment']}")
print(f"Categories: {result['categories']}")
print(f"Preference Updates: {result['preference_updates']}")
print(f"Insights: {result['insights']}")
print(f"Recommendations: {result['recommendations_for_future']}")
```

### Retrieve User Preferences

```python
prefs = await processor.get_user_preferences("user_123")

print(f"Detail Level: {prefs.detail_level}")
print(f"Tone: {prefs.document_tone}")
print(f"Formats: {prefs.preferred_formats}")
```

### Get Feedback Statistics

```python
stats = await processor.get_feedback_stats("user_123")

print(f"Total Feedback: {stats['total_feedback']}")
print(f"Average Rating: {stats['avg_rating']}")
print(f"Positive Count: {stats['positive_count']}")
print(f"Negative Count: {stats['negative_count']}")
```

## Processing Pipeline Flow

1. **Parse and Validate**
   - Create `UserFeedback` object
   - Parse rating to sentiment
   - Parse text feedback (if provided)

2. **Correlate to Execution**
   - Retrieve execution traces
   - Retrieve decision logs
   - Analyze correlations using LLM or heuristics

3. **Update Preferences**
   - Extract preference signals from text
   - Update user preferences in database
   - Return list of updates

4. **Update Historical Patterns**
   - Retrieve task details
   - Calculate success score
   - Create pattern entry in database

5. **Extract Insights**
   - Get recent feedback for pattern analysis
   - Convert preference updates to insights
   - Generate category-specific insights
   - Detect recurring patterns

6. **Generate Recommendations**
   - Filter high-confidence insights
   - Generate category-based recommendations
   - Return actionable list

7. **Save and Return**
   - Save feedback to database
   - Build result object
   - Return complete processing summary

## Database Schema

### user_feedback Collection

```json
{
  "feedback_id": "fb_abc123",
  "task_id": "task_123",
  "user_id": "user_123",
  "rating": 5,
  "text_feedback": "Great work!",
  "sentiment": "positive",
  "timestamp": "2026-02-14T12:00:00Z",
  "categories": ["quality", "speed"],
  "linked_steps": ["step_1", "step_2"],
  "linked_decisions": ["dec_1"]
}
```

### user_profiles Collection (preferences field)

```json
{
  "user_id": "user_123",
  "preferences": {
    "document_tone": "professional",
    "detail_level": "concise",
    "preferred_formats": ["markdown", "pdf"],
    "formatting_rules": {
      "include_citations": true
    }
  },
  "last_updated": "2026-02-14T12:00:00Z"
}
```

### historical_patterns Collection

```json
{
  "user_id": "user_123",
  "task_id": "task_123",
  "goal_request": "Generate market analysis",
  "plan_summary": "3 steps: research, analyze, write",
  "approach": "standard",
  "outcome": "Great work!",
  "success_score": 1.0,
  "tags": ["quality", "speed"],
  "metadata": {
    "rating": 5,
    "feedback_categories": ["quality"],
    "task_status": "COMPLETED",
    "duration_seconds": 45.2
  },
  "created_at": "2026-02-14T12:00:00Z"
}
```

## Error Handling

The FeedbackProcessor implements comprehensive error handling:

1. **LLM Failures**: Falls back to heuristic parsing
2. **Database Errors**: Logs error and continues processing
3. **Missing Data**: Gracefully handles missing tasks, traces, or decisions
4. **Invalid Input**: Validates ratings and handles edge cases

All errors are logged with appropriate context for debugging.

## Performance Considerations

1. **Async Operations**: All database operations are async
2. **Batch Retrieval**: Limits trace/decision queries to 100 items
3. **LLM Optimization**: Uses low temperature (0.2-0.3) for consistent parsing
4. **Token Management**: Limits LLM token usage (512-1024 tokens)

## Testing

Comprehensive test suite includes:

- **Unit Tests** (39 tests in `tests/unit/test_feedback_processor.py`):
  - Rating parsing
  - Heuristic parsing
  - LLM parsing with fallback
  - Correlation analysis
  - Preference updates
  - Historical patterns
  - Insight extraction
  - Pattern analysis
  - Full pipeline
  - Database operations

- **Integration Tests** (`tests/integration/test_feedback_integration.py`):
  - Full pipeline with real database
  - Multiple feedback pattern detection
  - Statistics aggregation

- **Examples** (`examples/feedback_processor_usage.py`):
  - Basic usage
  - Detailed feedback
  - Negative feedback correlation
  - Recurring pattern detection
  - Statistics
  - Preference persistence

## Future Enhancements

Potential improvements:

1. **Embeddings**: Add vector embeddings for semantic similarity search
2. **Advanced Analytics**: ML models for pattern detection
3. **Real-time Processing**: Stream processing for immediate insights
4. **A/B Testing**: Track preference effectiveness
5. **Multi-modal Feedback**: Support voice, video feedback
6. **Collaborative Filtering**: Cross-user pattern learning
7. **Explainability**: Enhanced reasoning for preference updates

## Integration with System

The FeedbackProcessor integrates with:

- **Memory Manager**: Stores/retrieves user preferences
- **Trace Logger**: Accesses execution traces and decisions
- **Database Adapter**: Persists all feedback data
- **Groq LLM**: Analyzes text feedback
- **Task Router**: Future tasks use updated preferences

## Configuration

Uses existing `settings` for:
- MongoDB connection
- Groq API key
- LLM model selection
- Temperature and token limits

No additional configuration required.
