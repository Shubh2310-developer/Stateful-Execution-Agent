# Phase 5: Executor & Tool Orchestration

This phase implements the tactical engine that carries out the steps defined by the Planner, manages the actual tools, and handles the output artifacts.

## Goals
- Implement the step-by-step execution loop.
- Build the tool registry and orchestration system.
- Implement artifact management and storage integration.
- Ensure atomic execution of steps with recovery points.

## 5.1 Step Runner (`src/executor/step_runner.py`)
- **Implementation**:
    - Logic to load a single step from the plan.
    - Preparation of inputs (retrieving previous artifacts if needed).
    - Invocation of the `ToolOrchestrator`.
    - Capturing outputs and updating the `TraceLogger`.
    - Verification: Checking the output against the step's `success_criteria`.

## 5.2 Tool Registry (`src/tools/tool_registry.py`)
- **Implementation**:
    - Base class `BaseTool` defining the interface (`execute`, `validate_input`, `get_schema`).
    - Tool Discovery: Auto-load tools from `src/tools/` subdirectories.
    - Schema generation for LLM context (presents tool capabilities to the Planner/Executor).

## 5.3 Core Tools Implementation
Implement the first set of functional tools:
- **`DocumentSearch`**: Search local/attached documents.
- **`WebSearch`**: Integration with Brave Search or Serper.
- **`Summarizer`**: LLM-powered text summarization.
- **`MetricsAnalyzer`**: Basic data processing (CSV/JSON to stats).
- **`PDFGenerator`**: Convert markdown/HTML to PDF.

## 5.4 Tool Orchestrator (`src/executor/tool_orchestrator.py`)
- **Implementation**:
    - Dynamic tool selection based on the step's `action`.
    - Parameter mapping: Mapping step inputs to tool parameters.
    - Error isolation: Catching tool-specific crashes and wrapping them in `ExecutionError`.

## 5.5 Artifact Manager (`src/storage/artifact_store.py`)
- **Implementation**:
    - Integration with local filesystem or S3-compatible storage.
    - `save_artifact(task_id, content, metadata)`: Persistence logic.
    - `get_artifact_preview(artifact_id)`: Generate short text snippet for LLM context.
    - Cleanup logic for temporary workspace files.

## Verification Criteria
- [ ] Step runner successfully executes a single "Summarize" step.
- [ ] Tool registry correctly lists all available tools and their schemas.
- [ ] Artifacts are saved to the designated storage and recorded in the task state.
- [ ] Tool failure correctly triggers a "FAILED" status with a clear error message in the trace.
