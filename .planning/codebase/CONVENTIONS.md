# Coding Conventions

**Analysis Date:** 2026-02-14

## Naming Patterns

**Files:**
- `snake_case.py` - Standard Python naming (e.g., `artifact_manager.py`, `task_schemas.py`).

**Functions:**
- `snake_case` - Descriptive names (e.g., `execute_plan`, `generate_response`).

**Variables:**
- `snake_case` - Used for local variables and instance attributes.

**Types:**
- `PascalCase` for classes (e.g., `TaskState`, `GroqClient`).
- Type hints are mandatory for function parameters and return values using the `typing` module or built-in types.

## Code Style

**Formatting:**
- `black` - Identified in `requirements.txt`.
- `isort` - Used for import sorting.

**Linting:**
- `flake8`, `pylint`, `mypy` - Identified in `requirements.txt`, indicating strict type checking and style enforcement.

## Import Organization

**Order:**
1. Standard library imports (e.g., `os`, `sys`, `datetime`).
2. Third-party library imports (e.g., `fastapi`, `pydantic`, `groq`).
3. Local application imports (e.g., `from src.core.config import settings`).

**Path Aliases:**
- `src.` is used as the base for all local imports.

## Error Handling

**Patterns:**
- Custom exception hierarchy defined in `src/core/exceptions.py` inheriting from `AgentError`.
- Use of `try...except` blocks with specific exception types.
- `logger.exception()` is used in `except` blocks to capture stack traces.
- API endpoints use `fastapi.HTTPException` for returning error responses to clients.

## Logging

**Framework:** `loguru`

**Patterns:**
- Configured in `src/utils/logger.py`.
- Intercepts standard `logging` calls.
- Output includes timestamps, levels, filenames, and line numbers.
- File-based logging for errors in `logs/error.log`.
- Usage: `logger.info()`, `logger.error()`, `logger.debug()`.

## Comments

**When to Comment:**
- Classes and complex methods have docstrings explaining their purpose.
- Logical sections within long methods are separated by comments.

**JSDoc/TSDoc:**
- Not applicable (Python project). Standard Python docstrings are used.

## Function Design

**Size:** Generally focused on single responsibility. Complex orchestrators like `Executor.execute_plan` manage high-level flow.

**Parameters:** Heavily use Pydantic models for complex input structures (e.g., `TaskState`, `TaskCreate`).

**Return Values:** Explicit type hints; async functions return `Awaitable` results.

## Module Design

**Exports:** Classes and functions are exported from `__init__.py` files to provide clean public APIs for sub-packages.

**Barrel Files:** `__init__.py` used to simplify imports (e.g., `from src.api.routes import tasks`).

---

*Convention analysis: 2026-02-14*
