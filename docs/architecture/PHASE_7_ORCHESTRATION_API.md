# Phase 7: Orchestration & API Layer

This phase connects the internal agent logic to the outside world, providing a robust FastAPI interface and managing the overall task lifecycle.

## Goals
- Build the FastAPI application structure.
- Implement the Session Manager and Task Router.
- Create the core REST endpoints for task lifecycle (Create, Status, Continue, Pause).
- Set up security and rate limiting.

## 7.1 Session Manager (`src/orchestration/session_manager.py`)
- **Implementation**:
    - Manage active task instances.
    - Handle session expiration and auto-saving of state.
    - Context isolation: Ensure one user's task doesn't bleed into another's.

## 7.2 Task Router (`src/orchestration/task_router.py`)
- **Implementation**:
    - Direct incoming requests to the appropriate module (Planner, Executor, or Reviewer).
    - Logic for "Continuation": When a user provides feedback mid-task, the router must decide whether to re-plan or resume execution.
    - Handle interruptions: Cleanly pause execution when a client disconnects or a timeout is reached.

## 7.3 API Core (`src/api/app.py` & `src/api/routes/`)
- **Library**: `FastAPI` + `Uvicorn`.
- **Endpoints**:
    - `POST /tasks`: Create a new task (trigger planning).
    - `GET /tasks/{id}`: Get status, progress, and current artifact list.
    - `POST /tasks/{id}/continue`: Provide feedback or approval to resume.
    - `POST /tasks/{id}/pause`: Manual suspension.
    - `GET /tasks/{id}/trace`: Retrieve the decision reasoning for the task.

## 7.4 Middleware (`src/api/middleware/`)
- **Implementation**:
    - `AuthMiddleware`: Verify API keys or JWTs.
    - `LoggingMiddleware`: Record all incoming requests and response times.
    - `RateLimiter`: Prevent abuse of the LLM and DB resources.
    - `ErrorHandler`: Catch all exceptions and return structured JSON error responses.

## 7.5 Background Tasks
- **Mechanism**:
    - Use FastAPI's `BackgroundTasks` or a dedicated worker (Celery/RQ) for long-running agent execution.
    - Ensure that background workers have access to the same state persistence layer.

## Verification Criteria
- [ ] API server starts successfully.
- [ ] `/health` endpoint returns 200 OK.
- [ ] Submitting a task via `POST /tasks` correctly initializes a task in the DB and returns a 201 Created.
- [ ] Background worker successfully executes a multi-step task to completion.
- [ ] Unauthorized requests are rejected with a 401.
