# Antigravity AI-UX Patterns

Designing for an autonomous agent requires specialized UI patterns that handle the unique nature of AI: uncertainty, feedback loops, and multi-step reasoning. This document defines the AI-UX patterns for the Antigravity UI.

## 1. The "Glass Box" Transparency Pattern

Instead of a "loading" spinner, we show the agent's work-in-progress to build trust and allow for early intervention.

- **Thinking States**: When the agent is planning or reasoning, use a "Thinking" indicator that displays high-level metadata about the current process (e.g., "Scanning 15 incident reports...", "Evaluating 3 alternative plans...").
- **Real-time Trace**: The Decision Trace is the primary feature. Every decision, tool call, and validation result must be visible in real-time.
- **Uncertainty Highlighting**: When the agent's confidence score is low (< 0.7), the UI should highlight the reasoning entry with a "Needs Review" indicator (Amber border).

## 2. Collaborative Feedback Loops

The UI must facilitate easy "Human-in-the-Loop" interactions without breaking the agent's autonomous flow.

- **Proactive Checkpoints**: For high-impact or irreversible steps (e.g., deleting a file, pushing code), the agent should pause and present a "Decision Request" card to the user.
- **Inline Corrections**: Users should be able to click any entry in the Decision Trace and provide feedback (e.g., "Actually, use the Q4 data for this").
- **Refinement Prompts**: After an artifact is generated, the UI presents a specialized "Refinement" input where the user can ask for adjustments (e.g., "Make the tone more professional").

## 3. Handling AI Failures & Errors

Failures are inevitable in agentic workflows. The UI must handle them gracefully.

- **Error Taxonomy Visualization**: Differentiate between "Transient Errors" (retrying automatically) and "Critical Blockers" (requiring user intervention).
- **Suggested Fixes**: When a step fails, the UI should present the agent's proposed alternative paths (e.g., "API Timeout. Should I try a different tool or skip this step?").
- **Rollback UI**: Allow users to "Time Travel" back to a previous state version if the agent's current path is incorrect.

## 4. Memory Visibility

The agent's "Learning" should be visible to the user.

- **"Learned Preference" Toasts**: When the agent applies a preference from long-term memory, show a subtle indicator (e.g., "Applying your preferred document tone...").
- **Preference Management**: A dedicated UI section where users can view and edit the "facts" and "patterns" the agent has learned about them.

## 5. Artifact Progress & Preview

- **Streaming Output**: For text-based artifacts (Markdown, Code), show the content as it is being streamed from the LLM.
- **Incremental Validation**: Show checkmarks next to success criteria as they are met during the generation process.
- **Version History**: Allow users to compare different versions of an artifact generated during the refinement loop.
