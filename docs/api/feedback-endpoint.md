# Feedback API Endpoint Documentation

## Overview

The Feedback API endpoint allows users to submit ratings and text feedback for completed tasks. The feedback is processed by the `FeedbackProcessor` to extract actionable insights, update user preferences, and improve future task execution.

## Endpoint

```
POST /api/v1/tasks/{task_id}/feedback
```

## Authentication

- Requires valid authentication token (if authentication middleware is enabled)
- Users can only submit feedback for their own tasks (session isolation)

## Request

### Path Parameters

| Parameter | Type   | Required | Description                |
|-----------|--------|----------|----------------------------|
| task_id   | string | Yes      | Unique identifier for task |

### Request Body

```json
{
  "rating": 4,
  "text_feedback": "Great work, but too verbose. Please be more concise."
}
```

| Field         | Type    | Required | Description                                    |
|---------------|---------|----------|------------------------------------------------|
| rating        | integer | Yes      | Rating on 1-5 scale (1=worst, 5=best)          |
| text_feedback | string  | No       | Optional detailed text feedback                |

### Validation

- `rating` must be between 1 and 5 (inclusive)
- `text_feedback` is optional but recommended for detailed insights

## Response

### Success Response (201 Created)

```json
{
  "feedback_id": "fb_abc123",
  "processed_at": "2026-02-14T12:00:00Z",
  "sentiment": "positive",
  "categories": ["quality", "speed"],
  "correlations": {
    "steps": {
      "step_1": 0.9,
      "step_3": 0.7
    },
    "decisions": {
      "dec_2": 0.8
    }
  },
  "preference_updates": [
    {
      "field": "detail_level",
      "old_value": "medium",
      "new_value": "concise",
      "confidence": 0.85,
      "reasoning": "User indicated preference for concise responses"
    }
  ],
  "historical_pattern_updated": true,
  "insights": [
    {
      "insight": "User preference identified: detail_level",
      "confidence": 0.85,
      "action": "Set default detail_level to 'concise'",
      "category": "preference",
      "metadata": {
        "field": "detail_level",
        "new_value": "concise"
      }
    }
  ],
  "recommendations_for_future": [
    "Set default detail_level to 'concise'",
    "Apply updated user preferences to all future tasks"
  ]
}
```

### Response Fields

| Field                       | Type    | Description                                              |
|-----------------------------|---------|----------------------------------------------------------|
| feedback_id                 | string  | Unique identifier for this feedback                       |
| processed_at                | string  | ISO 8601 timestamp of processing                          |
| sentiment                   | string  | Overall sentiment: "positive", "neutral", or "negative"   |
| categories                  | array   | Detected categories (quality, speed, accuracy, etc.)      |
| correlations                | object  | Links to specific steps and decisions                     |
| preference_updates          | array   | List of user preference updates made                      |
| historical_pattern_updated  | boolean | Whether a historical pattern was created                  |
| insights                    | array   | Actionable insights extracted from feedback               |
| recommendations_for_future  | array   | Recommendations for future task execution                 |

### Error Responses

#### 404 Not Found
Task does not exist.

```json
{
  "detail": "Task test_task_123 not found"
}
```

#### 403 Forbidden
User attempting to provide feedback for another user's task.

```json
{
  "detail": "Not authorized to provide feedback for this task"
}
```

#### 422 Validation Error
Invalid request body (e.g., rating out of range).

```json
{
  "detail": [
    {
      "loc": ["body", "rating"],
      "msg": "ensure this value is greater than or equal to 1",
      "type": "value_error.number.not_ge"
    }
  ]
}
```

#### 500 Internal Server Error
Feedback processing failed.

```json
{
  "detail": "Feedback processing failed: <error message>"
}
```

## Examples

### Example 1: Basic Rating Feedback

**Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/tasks/task_123/feedback" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "rating": 5
  }'
```

**Response:**
```json
{
  "feedback_id": "fb_xyz789",
  "processed_at": "2026-02-14T14:30:00Z",
  "sentiment": "positive",
  "categories": [],
  "correlations": {
    "steps": {},
    "decisions": {}
  },
  "preference_updates": [],
  "historical_pattern_updated": true,
  "insights": [],
  "recommendations_for_future": []
}
```

### Example 2: Detailed Text Feedback

**Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/tasks/task_456/feedback" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "rating": 4,
    "text_feedback": "Great analysis, but the report was too verbose. I prefer concise summaries with bullet points. Also, please include more citations next time."
  }'
```

**Response:**
```json
{
  "feedback_id": "fb_def456",
  "processed_at": "2026-02-14T15:00:00Z",
  "sentiment": "positive",
  "categories": ["format", "completeness"],
  "correlations": {
    "steps": {
      "step_research": 0.75,
      "step_write": 0.9
    },
    "decisions": {}
  },
  "preference_updates": [
    {
      "field": "detail_level",
      "old_value": "medium",
      "new_value": "concise",
      "confidence": 0.8,
      "reasoning": "User indicated preference for concise responses"
    },
    {
      "field": "formatting_rules.include_citations",
      "old_value": false,
      "new_value": true,
      "confidence": 0.85,
      "reasoning": "User values citations and sources"
    }
  ],
  "historical_pattern_updated": true,
  "insights": [
    {
      "insight": "User preference identified: detail_level",
      "confidence": 0.8,
      "action": "Set default detail_level to 'concise'",
      "category": "preference",
      "metadata": {
        "field": "detail_level",
        "new_value": "concise"
      }
    },
    {
      "insight": "User preference identified: formatting_rules.include_citations",
      "confidence": 0.85,
      "action": "Set default formatting_rules.include_citations to 'True'",
      "category": "preference",
      "metadata": {
        "field": "formatting_rules.include_citations",
        "new_value": true
      }
    }
  ],
  "recommendations_for_future": [
    "Set default detail_level to 'concise'",
    "Set default formatting_rules.include_citations to 'True'",
    "Apply updated user preferences to all future tasks"
  ]
}
```

### Example 3: Negative Feedback

**Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/tasks/task_789/feedback" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "rating": 2,
    "text_feedback": "The analysis was incomplete and contained several errors. Missing key data points."
  }'
```

**Response:**
```json
{
  "feedback_id": "fb_ghi789",
  "processed_at": "2026-02-14T16:00:00Z",
  "sentiment": "negative",
  "categories": ["completeness", "accuracy"],
  "correlations": {
    "steps": {
      "step_analyze": 0.85
    },
    "decisions": {
      "dec_data_source": 0.7
    }
  },
  "preference_updates": [],
  "historical_pattern_updated": true,
  "insights": [
    {
      "insight": "User reported accuracy issues",
      "confidence": 0.85,
      "action": "Increase validation rigor and fact-checking",
      "category": "quality",
      "metadata": {
        "category": "accuracy"
      }
    },
    {
      "insight": "User found output incomplete",
      "confidence": 0.8,
      "action": "Ensure all success criteria are thoroughly addressed",
      "category": "quality",
      "metadata": {
        "category": "completeness"
      }
    }
  ],
  "recommendations_for_future": [
    "Increase validation rigor and fact-checking",
    "Ensure all success criteria are thoroughly addressed",
    "Increase validation checks before task completion"
  ]
}
```

## Processing Pipeline

When feedback is submitted, the following steps occur:

1. **Validation**: Task existence and user authorization are verified
2. **Sentiment Analysis**: Rating is mapped to sentiment (positive/neutral/negative)
3. **Text Parsing**: LLM extracts structured information from text feedback
4. **Correlation**: Feedback is correlated to specific execution steps and decisions
5. **Preference Updates**: User preferences are extracted and updated in database
6. **Pattern Storage**: Historical pattern is created for future reference
7. **Insight Extraction**: Actionable insights are generated with confidence scores
8. **Recommendations**: Future task recommendations are generated

## Integration

### Using with MemoryManager

User preferences updated through feedback are automatically used by the `MemoryManager` in future tasks:

```python
from src.memory.memory_manager import MemoryManager

memory_manager = MemoryManager()
user_memory = await memory_manager.get_user_memory(user_id)

# Preferences are automatically applied
print(user_memory.preferences.detail_level)  # "concise" (from feedback)
print(user_memory.preferences.formatting_rules)  # {"include_citations": True}
```

### Using with Planner

The `AdaptivePlanner` can leverage historical patterns to improve planning:

```python
from src.planner.adaptive_planner import AdaptivePlanner

planner = AdaptivePlanner()
plan = await planner.plan_task(task_state)

# Planner uses historical patterns and user preferences from feedback
```

## Best Practices

1. **Encourage Text Feedback**: Text feedback provides richer insights than ratings alone
2. **Submit After Completion**: Feedback is most valuable after task completion
3. **Be Specific**: Mention specific aspects (speed, accuracy, format) for better correlation
4. **Regular Feedback**: Consistent feedback helps the system learn user preferences
5. **Constructive Criticism**: Negative feedback should explain what was missing or wrong

## Security

- **Authentication**: Endpoint respects authentication middleware
- **Authorization**: Users can only submit feedback for their own tasks
- **Validation**: All inputs are validated before processing
- **Error Handling**: Sensitive errors are logged server-side, generic messages returned to client

## Performance

- **Async Processing**: All operations are async for better performance
- **LLM Caching**: Repeated feedback patterns are cached
- **Database Optimization**: Batch operations and indexed queries
- **Token Limits**: LLM calls are limited to 512-1024 tokens for efficiency

## Future Enhancements

- **Batch Feedback**: Submit feedback for multiple tasks at once
- **Feedback Analytics**: Dashboard showing feedback trends over time
- **Sentiment Trends**: Track sentiment changes across tasks
- **Automated Recommendations**: Proactive suggestions based on feedback patterns
- **Export Feedback**: Download feedback history as CSV/JSON
