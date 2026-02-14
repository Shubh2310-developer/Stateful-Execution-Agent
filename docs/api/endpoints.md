# API Endpoints Specification

The Stateful Execution Agent provides a RESTful API for managing the lifecycle of autonomous tasks. All endpoints are prefixed with `/api/v1`.

## Task Management

### Create Task
`POST /tasks/create`

Initializes a new task and triggers the planning phase.

**Request Body:**
```json
{
  "user_id": "string",
  "goal": "string",
  "context": {},
  "execution_mode": "autonomous"
}
```

### Get Task Status
`GET /tasks/{task_id}/status`

Retrieves the current status, progress, and active step of a task.

### Continue Task
`POST /tasks/{task_id}/continue`

Resumes a paused or failed task, optionally providing new input or feedback.

**Request Body:**
```json
{
  "user_input": "string",
  "mode": "resume"
}
```

## State and Traceability

### Get Task State
`GET /state/{task_id}`

Returns the full current state object for a task, including the plan and artifacts map.

### Get Decision Trace
`GET /trace/{task_id}`

Retrieves the detailed log of all decisions and actions taken during task execution.

## Artifacts

### List Task Artifacts
`GET /artifacts/task/{task_id}`

Returns a list of all artifacts produced by a specific task.

## Memory

### Get User Memory
`GET /memory/{user_id}`

Retrieves the persistent long-term memory, preferences, and patterns for a user.

## System

### Health Check
`GET /health`

Returns the current operational status of the API and its dependencies.
