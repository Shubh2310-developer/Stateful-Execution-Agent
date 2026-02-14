# Architecture

**Analysis Date:** 2026-02-14

## Pattern Overview

**Overall:** Layered Micro-Orchestration Architecture. The system follows a modular design where distinct components handle planning, execution, memory management, and state persistence, coordinated by a central workflow engine.

**Key Characteristics:**
- **Stateful Execution:** Every task has a persistent `TaskState` that tracks progress, artifacts, and decisions.
- **Plan-Execute-Review Loop:** The system decomposes goals into steps, executes them using tools, and validates the output.
- **Traceability:** Detailed decision logs and event traces are recorded for every action taken by the agent.

## Layers

**API Layer:**
- Purpose: Provides external endpoints for task management and system monitoring.
- Location: `src/api/`
- Contains: FastAPI routes, middleware, and request/response schemas.
- Depends on: `src/orchestration/`, `src/core/`
- Used by: External clients, integration scripts.

**Orchestration Layer:**
- Purpose: Coordinates the high-level workflow and session lifecycle.
- Location: `src/orchestration/`
- Contains: `WorkflowEngine` and `SessionManager`.
- Depends on: `src/planner/`, `src/executor/`, `src/state/`
- Used by: `src/api/`

**Domain Logic Layers (Planner/Executor/Reviewer):**
- Purpose: Handle specific phases of the task lifecycle.
- Location: `src/planner/`, `src/executor/`, `src/reviewer/`
- Contains: Goal parsing, step generation, tool orchestration, and validation logic.
- Depends on: `src/tools/`, `src/llm/`, `src/core/`
- Used by: `src/orchestration/`

**Capabilities & Support Layers:**
- Purpose: Provide shared functionality like LLM access, memory retrieval, and tool execution.
- Location: `src/llm/`, `src/memory/`, `src/tools/`, `src/trace/`
- Contains: LLM clients, semantic search, tool registries, and trace loggers.
- Depends on: `src/utils/`, `src/core/`
- Used by: Planner and Executor layers.

**Data & Persistence Layer:**
- Purpose: Handles storage and retrieval of state, artifacts, and memory.
- Location: `src/state/`, `src/storage/`
- Contains: Database adapters, serialization logic, and artifact stores.
- Depends on: `src/core/`
- Used by: Orchestration, Executor, and Memory layers.

## Data Flow

**Task Processing Flow:**

1. **Request:** Client sends a goal to `src/api/routes/tasks.py`.
2. **Session Initialization:** `SessionManager` initializes `TaskState` via `StateManager`.
3. **Planning:** `WorkflowEngine` triggers `Planner` to generate a `Plan` (list of `Step` objects).
4. **Execution:** `Executor` iterates through steps, using `StepRunner` to invoke `tools`.
5. **Traceability:** Each step and decision is logged via `TraceLogger`.
6. **State Update:** `StateManager` persists the updated `TaskState` after each significant change.
7. **Completion:** `WorkflowEngine` marks the task as completed and returns the final state.

**State Management:**
- State is handled through a centralized `TaskState` model defined in `src/core/types.py`.
- Persistence is managed by `src/state/state_manager.py` using pluggable adapters in `src/state/persistence/`.

## Key Abstractions

**TaskState:**
- Purpose: The "source of truth" for a task's current progress and history.
- Examples: `src/core/types.py` (class `TaskState`), `src/state/state_schema.py`.
- Pattern: State Pattern / Snapshot.

**BaseTool:**
- Purpose: Abstract base class for all agent capabilities.
- Examples: `src/tools/base_tool.py`.
- Pattern: Strategy Pattern.

**WorkflowEngine:**
- Purpose: Decouples the API from the complex logic of moving a task through its lifecycle.
- Examples: `src/orchestration/workflow_engine.py`.
- Pattern: Facade / Orchestrator.

## Entry Points

**API Server:**
- Location: `src/api/app.py`
- Triggers: HTTP requests.
- Responsibilities: Routing, auth, logging, and invoking the workflow engine.

**Examples/Scripts:**
- Location: `examples/*.py`
- Triggers: CLI execution.
- Responsibilities: Demonstrate specific features like task creation or trace analysis.

## Error Handling

**Strategy:** Multi-level error handling with middleware for API errors and status transitions for task failures.

**Patterns:**
- **Status-based Recovery:** If a step fails, the task status is set to `failed` or `paused`, allowing for manual intervention or re-planning.
- **Global Middleware:** `src/api/middleware/error_handler.py` catches unhandled exceptions at the API level.

## Cross-Cutting Concerns

**Logging:** Centralized logging via `src/utils/logger.py` and detailed execution tracing via `src/trace/trace_logger.py`.
**Validation:** Pydantic models in `src/core/types.py` for data validation; `ValidationEngine` in `src/executor/` for step output validation.
**Authentication:** Managed via FastAPI dependencies in `src/api/dependencies/auth.py`.

---

*Architecture analysis: 2026-02-14*
