# Codebase Structure

**Analysis Date:** 2026-02-14

## Directory Layout

```
[project-root]/
├── config/             # Configuration files for different environments
├── data/               # Data schemas, migrations, and seeds
├── docs/               # Technical documentation and roadmap
├── examples/           # Usage examples for various system features
├── infrastructure/     # Deployment configurations (Docker, K8s, Terraform)
├── scripts/            # Utility and maintenance scripts
├── src/                # Primary source code
│   ├── api/            # REST API implementation (FastAPI)
│   ├── core/           # Core types, constants, and global config
│   ├── executor/       # Step execution and tool orchestration
│   ├── llm/            # LLM provider clients and prompt management
│   ├── memory/         # Long-term and short-term memory systems
│   ├── orchestration/  # High-level workflow and session management
│   ├── planner/        # Goal decomposition and plan generation
│   ├── reviewer/       # Output validation and quality assurance
│   ├── state/          # Task state management and persistence
│   ├── storage/        # File and artifact storage adapters
│   ├── tools/          # Tool registry and implementation modules
│   ├── trace/          # Execution tracing and audit logging
│   └── utils/          # Shared utilities (logging, metrics)
└── tests/              # Comprehensive test suite
```

## Directory Purposes

**src/api:**
- Purpose: Provides the external interface to the system.
- Contains: Route handlers, middleware for auth/logging, and API-specific schemas.
- Key files: `src/api/app.py`, `src/api/routes/tasks.py`.

**src/orchestration:**
- Purpose: Manages the lifecycle of a task from request to completion.
- Contains: Workflow engine and session state tracking.
- Key files: `src/orchestration/workflow_engine.py`, `src/orchestration/session_manager.py`.

**src/planner:**
- Purpose: Transforms user goals into actionable plans.
- Contains: Goal parsers, step generators, and dependency analyzers.
- Key files: `src/planner/planner.py`, `src/planner/step_generator.py`.

**src/executor:**
- Purpose: Carries out the steps defined in a plan.
- Contains: Step runners, artifact managers, and validation logic.
- Key files: `src/executor/executor.py`, `src/executor/step_runner.py`.

**src/state:**
- Purpose: Ensures task continuity through persistence.
- Contains: Persistence adapters (DB, Cache) and serialization logic.
- Key files: `src/state/state_manager.py`, `src/state/persistence/database_adapter.py`.

**src/core:**
- Purpose: Defines the fundamental building blocks used across the codebase.
- Contains: Pydantic models for core entities and global settings.
- Key files: `src/core/types.py`, `src/core/config.py`.

## Key File Locations

**Entry Points:**
- `src/api/app.py`: FastAPI application entry point.

**Configuration:**
- `src/core/config.py`: Configuration loading logic.
- `config/default.yaml`: Base configuration settings.

**Core Logic:**
- `src/orchestration/workflow_engine.py`: Main execution flow coordinator.
- `src/core/types.py`: Definition of `TaskState`, `Plan`, and `Step`.

**Testing:**
- `tests/`: Root directory for all unit and integration tests.

## Naming Conventions

**Files:**
- snake_case: `workflow_engine.py`, `task_schemas.py`.

**Directories:**
- snake_case: `step_runner/`, `data_processor/`.

**Classes:**
- PascalCase: `WorkflowEngine`, `TaskState`.

## Where to Add New Code

**New Feature (e.g., a new processing phase):**
- Primary code: Create a new directory under `src/` (e.g., `src/optimizer/`).
- Integration: Update `src/orchestration/workflow_engine.py` to include the new phase.

**New Tool:**
- Implementation: Add to a relevant category in `src/tools/` (e.g., `src/tools/web/new_scraper.py`).
- Registration: Register the tool in `src/tools/tool_registry.py`.

**New API Endpoint:**
- Implementation: Add a router file to `src/api/routes/` or update an existing one.
- Registration: Include the router in `src/api/app.py`.

**Utilities:**
- Shared helpers: Add to `src/utils/` if generally applicable, or to the specific module's `utils/` if localized.

## Special Directories

**artifacts/:**
- Purpose: Local storage for files generated during task execution.
- Generated: Yes
- Committed: No (README only)

**data/schemas/:**
- Purpose: JSON schema definitions for core state objects.
- Generated: No
- Committed: Yes

---

*Structure analysis: 2026-02-14*
