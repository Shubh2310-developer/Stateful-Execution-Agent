# Phase 2: LLM Integration & Prompt Engineering

This phase implements the communication layer with the LLM provider (Groq) and the structured prompt management system.

## Goals
- Securely integrate with the Groq API.
- Implement robust retry and error handling for LLM calls.
- Create a template-based prompt management system.
- Implement token usage tracking and cost estimation.

## 2.1 Groq Client Integration (`src/llm/groq_client.py`)
- **Library**: `groq` Python SDK.
- **Implementation**:
    - Singleton client pattern.
    - Configuration for model selection (e.g., `llama3-70b-8192`, `mixtral-8x7b-32768`).
    - Async support for non-blocking I/O.
    - Support for streaming responses (optional but recommended for UX).

## 2.2 Prompt Engineering System (`src/llm/prompt_builder.py`)
- **Library**: `Jinja2`.
- **Implementation**:
    - Separate System Prompts from User Input templates.
    - Load templates from `src/planner/prompts/` and `src/executor/prompts/`.
    - Context Injection: Utility to safely inject state snippets, memory, and tool descriptions into prompts.
    - **Few-Shot Management**: System to inject relevant examples from `few_shot_examples.py` based on task type.

## 2.3 Reliability Layer (`src/llm/retry_handler.py`)
- **Library**: `Tenacity`.
- **Implementation**:
    - Exponential backoff for rate limits (429).
    - Retry logic for transient timeouts (504/503).
    - Maximum retry count (default 3-5).
    - Detailed logging of retry attempts in the decision trace.

## 2.4 LLM Observability (`src/llm/token_counter.py`)
- **Implementation**:
    - Token counting per request/response (using model-specific tokenizers if available or approximation).
    - Cost tracking based on configured pricing per model.
    - Integration with `src/utils/metrics.py` for Prometheus/Grafana exporting.

## 2.5 Response Parsing (`src/llm/response_parser.py`)
- **Implementation**:
    - Robust JSON extraction (handling markdown code blocks vs raw text).
    - Validation of LLM output against Pydantic models.
    - Fallback strategies for malformed JSON (e.g., asking for repair).

## Verification Criteria
- [x] Successful "Hello World" with Groq client.
- [x] Prompt templates correctly render with injected variables.
- [x] Retries trigger on simulated network failure.
- [x] Token usage accurately reported in logs.
- [x] JSON response parser handles varied LLM output formats.
