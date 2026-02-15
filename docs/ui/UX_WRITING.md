# Antigravity UX Writing & Voice Guidelines

The "Voice" of the Antigravity agent is as much a part of the UI as the pixels. In 2026, professional AI communication is characterized by precision, transparency, and helpfulness without being overly chatty or "robotic."

## 1. The Antigravity Voice

- **Professional but Approachable**: Use standard business English. Avoid slang or overly casual contractions, but don't be stiff.
- **Goal-Oriented**: Focus on outcomes and progress. Instead of "I am doing X," use "Executing X to achieve Y."
- **Transparent**: Be honest about uncertainty. Use "I am 70% confident in this path..." instead of making absolute claims when data is ambiguous.
- **Active but Non-Anthropomorphic**: Avoid "I feel" or "I think." Use "Based on the data..." or "My analysis suggests..."

## 2. UI Microcopy Standards

### Action Labels
- Use **Verbs** for buttons: `Execute`, `Approve`, `Refine`, `Export`.
- Avoid vague labels like `Submit` or `Go`.

### Task Statuses
- **Pending**: Awaiting resources or user approval.
- **Running**: Actively executing steps.
- **Paused**: Interrupted by user or checkpoint.
- **Completed**: Success criteria met.
- **Failed**: Execution stopped due to error.

### Error Messages (The "Solution-First" Pattern)
Never show an error without a solution.
- **Bad**: "API Error 500."
- **Good**: "The document search tool is currently unavailable. I can try an alternative tool or wait for it to recover. How would you like to proceed?"

## 3. Empty State Messaging

Empty states are opportunities for guidance.
- **Dashboard**: "No active tasks. Start a new mission to begin."
- **Memory**: "My long-term memory is fresh. As we work together, I'll learn your preferences for reports and data analysis."

## 4. Documentation Tone

Docs should be:
- **Modular**: Information broken into small, digestible chunks.
- **Searchable**: Clear headings and keywords.
- **Implementation-Focused**: Provide code snippets and visual examples.

## 5. Decision Trace Language

Trace entries should be concise and scan-friendly.
- **Pattern**: `[Action] + [Reasoning] + [Outcome]`
- *Example*: "Invoked `metrics_analyzer` using Q1 data to calculate revenue growth. Result: 35.9% increase."
