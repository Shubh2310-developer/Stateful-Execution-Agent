# Testing Patterns

**Analysis Date:** 2026-02-14

## Test Framework

**Runner:**
- `pytest` (>=7.0.0, <8.0.0)
- Config: `pyproject.toml` (likely, though file was empty, requirements specify pytest).

**Assertion Library:**
- Native `assert` statement.

**Run Commands:**
```bash
pytest                 # Run all tests
pytest --watch         # Watch mode (requires pytest-watch if installed)
pytest --cov=src       # Coverage
```

## Test File Organization

**Location:**
- Separate `tests/` directory mirroring `src/` structure.

**Naming:**
- Files: `test_*.py` (e.g., `tests/unit/test_executor/test_step_runner.py`).
- Functions: `test_*`.

**Structure:**
```
tests/
├── fixtures/          # Shared test data
├── unit/              # Isolated component tests
├── integration/       # Multi-component/API tests
└── performance/       # Load and latency tests
```

## Test Structure

**Suite Organization:**
```python
import pytest

@pytest.mark.asyncio
async def test_feature_behavior():
    # Arrange
    # Act
    # Assert
    pass
```

**Patterns:**
- **Arrange-Act-Assert** pattern is the standard.
- Extensive use of `@pytest.mark.asyncio` for async functions.

## Mocking

**Framework:** `pytest-mock` (based on `unittest.mock`).

**Patterns:**
```python
def test_something(mocker):
    mock_client = mocker.patch("src.llm.groq_client.Groq")
    # ...
```

**What to Mock:**
- External APIs (Groq, AWS S3).
- Databases (MongoDB, PostgreSQL).
- Message Queues (Kafka).

**What NOT to Mock:**
- Core data models (Pydantic models).
- Pure utility functions.

## Fixtures and Factories

**Test Data:**
```python
# From tests/fixtures/sample_tasks.py (intended pattern)
@pytest.fixture
def sample_task_state():
    return TaskState(task_id="test-123", ...)
```

**Location:**
- `tests/fixtures/` contains shared fixtures for artifacts, plans, tasks, and user data.

## Coverage

**Requirements:** `pytest-cov` is used to track coverage.

**View Coverage:**
```bash
pytest --cov=src --cov-report=html
```

## Test Types

**Unit Tests:**
- Focus on individual classes and methods in `tests/unit/`.
- Heavy use of mocking for dependencies.

**Integration Tests:**
- Test API endpoints and end-to-end workflows in `tests/integration/`.
- Test error recovery and memory learning.

**E2E Tests:**
- Represented by `test_end_to_end_workflow.py`.

## Common Patterns

**Async Testing:**
- Use `pytest-asyncio` with `@pytest.mark.asyncio`.

**Error Testing:**
```python
with pytest.raises(AgentError):
    await some_failing_function()
```

---

*Testing analysis: 2026-02-14*
