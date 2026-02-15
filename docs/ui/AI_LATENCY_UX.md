# Antigravity AI Latency Handling UX

LLM reasoning and complex tool execution can be slow. This document defines the UX patterns for managing latency while maintaining a high-performance feel.

## 1. Time-to-First-Token (TTFT) Optimization
- **Thinking Indicators**: Use a high-fidelity "Thinking" shimmer or a textual "Streaming Log" of the agent's internal thought process as it arrives.
- **Micro-milestones**: As the agent finishes planning or gathers a specific source, update the status immediately (e.g., "Plan Generated -> Searching docs...").

## 2. Streaming Artifacts
- **Real-time Markdown**: Render text as it streams from the LLM. Use a "Ghost Cursor" to signal active writing.
- **Incremental Tables**: Populating rows in a table as data is extracted, rather than waiting for the full dataset.

## 3. Background Persistence
- **"Set it and Forget it"**: A clear UI affordance that a task is running in the background and the user can safely close the tab or move to another view.
- **Handoff Toasts**: Non-distractive notifications that a long-running step has finished.

## 4. Latency Awareness
- **Health Indicators**: (See [SYSTEM_HEALTH_UX.md](./SYSTEM_HEALTH_UX.md)) — Visual confirmation if the LLM provider is currently slow, reducing user frustration.
- **Historical Comparison**: "This task usually takes 5 minutes. Current progress: 2 minutes."

## 5. Predictive UI
- **Skeleton Buffering**: Pre-rendering the structure of the next step's workplace based on the generated plan, even before the data arrives.
- **Local Pre-validation**: Checking user inputs locally before sending them to the agent to avoid unnecessary round-trips.
