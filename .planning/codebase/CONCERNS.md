# Codebase Concerns

**Analysis Date:** 2026-02-14

## Tech Debt

**LLM Client Initialization:**
- Issue: `GroqClient` is instantiated as a global singleton in `src/llm/groq_client.py`, making it difficult to mock for tests or rotate configurations dynamically.
- Files: `src/llm/groq_client.py`
- Impact: Testing difficulty and lack of flexibility in model management.
- Fix approach: Move to a dependency injection pattern or a factory pattern.

**Hardcoded Execution Logic:**
- Issue: Step execution defaults artifact types and formats rather than deriving them from tool metadata or step requirements.
- Files: `src/executor/step_runner.py` (lines 71-73)
- Impact: Limited support for diverse artifact types (images, files, etc.).
- Fix approach: Implement a more robust `ArtifactManager` that uses tool-defined schemas for artifact creation.

**Synchronous Blocking in Async Code:**
- Issue: The retry decorator uses `time.sleep()` which blocks the entire Python event loop in an asynchronous application.
- Files: `src/llm/retry_handler.py` (line 26)
- Impact: Severe performance degradation; the server cannot process other requests while waiting for a retry.
- Fix approach: Replace `time.sleep(sleep_time)` with `await asyncio.sleep(sleep_time)` and ensure the decorator supports async functions.

## Known Bugs

**Event Loop Blocking:**
- Symptoms: The application becomes unresponsive during LLM API retries.
- Files: `src/llm/retry_handler.py`
- Trigger: LLM API failures causing the `retry_with_exponential_backoff` decorator to trigger.
- Workaround: None currently implemented.

**Incomplete Session Management:**
- Symptoms: `user_id` is passed manually in some requests but assumed in others.
- Files: `src/api/routes/tasks.py` (line 60)
- Trigger: Using the `/{task_id}/continue` endpoint.
- Workaround: Manually ensuring the state contains the `user_id`.

## Security Considerations

**Default Secret Keys:**
- Risk: `SECRET_KEY` and other sensitive defaults are committed to the codebase and might be used in production.
- Files: `src/core/config.py` (line 11)
- Current mitigation: Warning comment in the code.
- Recommendations: Enforce environment variable presence for production builds and use a secrets manager.

**Authentication Gaps:**
- Risk: Task continuation assumes simplicity and doesn't strictly validate user ownership beyond what's in the state.
- Files: `src/api/routes/tasks.py` (lines 60-71)
- Current mitigation: Minimal.
- Recommendations: Implement proper JWT or session-based authentication in the `auth.py` dependency and apply it to all task routes.

## Performance Bottlenecks

**LLM Context Truncation:**
- Problem: Validation engine truncates output to 2000 characters, potentially missing crucial failure indicators in large outputs.
- Files: `src/executor/validation_engine.py` (line 37)
- Cause: Arbitrary limit to stay within prompt token bounds.
- Improvement path: Implement a more sophisticated context window management or use a "summary-first" validation approach for large artifacts.

**Database Upserts:**
- Problem: `save_state` performs a full document `$set` on every state update.
- Files: `src/state/persistence/database_adapter.py` (lines 19-23)
- Cause: Simple implementation using `update_one` with `upsert=True`.
- Improvement path: Use atomic updates (`$set` only changed fields) to reduce database load and network traffic for large state objects.

## Fragile Areas

**JSON Response Parsing:**
- Files: `src/executor/step_runner.py` (line 44), `src/executor/validation_engine.py` (line 47)
- Why fragile: Highly dependent on the LLM's ability to strictly follow JSON formatting instructions. Small deviations cause total step failure.
- Safe modification: Use a library like `instructor` or implement robust regex-based JSON extraction with repair logic.
- Test coverage: Minimal evidence of robust error handling for malformed LLM responses.

**Sequential Execution Loop:**
- Files: `src/executor/executor.py` (lines 32-71)
- Why fragile: If a step fails validation but doesn't properly trigger a `break` or state transition, the loop could behave unexpectedly or stall.
- Safe modification: Implement a formal state machine for task transitions.
- Test coverage: Integrated tests exist but edge cases for loop interruption are unclear.

## Test Coverage Gaps

**Tool Orchestration:**
- What's not tested: Complex tool interactions and failure modes for individual tools.
- Files: `src/executor/tool_orchestrator.py`, `src/tools/*`
- Risk: Unexpected tool behavior could crash the executor.
- Priority: Medium

**Trace Analytics:**
- What's not tested: Pattern detection and performance aggregation logic.
- Files: `src/trace/analytics/*`
- Risk: Decisions based on incorrect analytics or missed optimization opportunities.
- Priority: Low

---

*Concerns audit: 2026-02-14*
