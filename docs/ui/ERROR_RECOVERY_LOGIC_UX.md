# Antigravity Error Recovery Logic UX

When an autonomous agent encounters a failure, its recovery process should be as transparent as its successful execution. This document defines how recovery logic is visualized.

## 1. The Failure Anatomy
- **Source Identification**: Clearly mark where the failure happened (e.g., in a specific Tool, a reasoning step, or an LLM response).
- **Categorization**: Use the [Error State](./ERROR_STATES.md) patterns to distinguish between "Logic Failures" and "Infrastructure Failures."

## 2. Recovery Path Visualization
- **The Decision Tree**: When a failure occurs, the agent evaluates recovery options. Show this as a small, localized branching graph.
- **Proposed Paths**:
  - `Path A: Retry Tool` (Confidence: 80%)
  - `Path B: Alternate Tool` (Confidence: 60%)
  - `Path C: Human Help` (Confidence: 100%)

## 3. Automated Recovery Trace
- **Reasoning for Recovery**: The trace entry should explain *why* a specific recovery path was chosen.
  - *Example*: "Tool `web_search` failed with 504. Since this is a transient error, I am applying the exponential backoff policy (Attempt 1)."
- **Retry Counters**: A small circular indicator `(1/3)` showing the progress of automated retry attempts.

## 4. Manual Intervention Surface
- **Correction Context**: When human help is requested, the UI should provide a "Pre-filled Correction" — the agent's best guess at what is wrong, which the user can simply edit and submit.
- **Step Rewind**: A visual control to "Rewind" the agent's state by one or two steps to try a different logical approach before the failure point.

## 5. Learning from Recovery
- **Pattern extraction**: If a manual recovery is successful, show a "Learning Saved" indicator: "I've learned to use `Source B` when `Source A` times out."
- **Recovery Analytics**: A dashboard widget showing the most common failure points and the effectiveness of automated vs. manual recoveries.
