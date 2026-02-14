# Example: Basic Task Lifecycle

This example walks through the creation and completion of a simple research task.

## The Goal
"Research the benefits of stateful agents vs stateless agents."

## 1. Creating the Task

Send a POST request to `/api/v1/tasks/create`:

```json
{
  "user_id": "usr_dev_123",
  "goal": "Research the benefits of stateful agents vs stateless agents and provide a summary.",
  "execution_mode": "autonomous"
}
```

**Response:**
```json
{
  "task_id": "task_abc123",
  "status": "planned",
  "goal_summary": "Research and summarize stateful vs stateless agents"
}
```

## 2. Monitoring Progress

Retrieve the status via `GET /api/v1/tasks/task_abc123/status`:

```json
{
  "status": "in_progress",
  "progress": {
    "completed_steps": 1,
    "total_steps": 3,
    "percentage": 33.3,
    "current_step": "step_002: summarize_findings"
  }
}
```

## 3. Retrieving the Result

Once status is `completed`, list the artifacts via `GET /api/v1/artifacts/task/task_abc123`:

```json
[
  {
    "artifact_id": "art_xyz789",
    "type": "document",
    "format": "md",
    "storage_uri": "file:///app/artifacts/research_summary.md"
  }
]
```

## 4. Reviewing Decisions

Check the reasoning behind the agent's actions via `GET /api/v1/trace/task_abc123`:

- Decision 1: "Selected 'web_search' to find recent comparisons."
- Decision 2: "Filtering results to focus on architectural differences."
- Decision 3: "Formatting as a technical comparison document per user preferences."
