# Antigravity Context Window UX

The context window is a finite resource in LLM-driven agents. This document defines how the UI visualizes "Context Pressure" and the agent's strategy for managing it.

## 1. Context Pressure Gauges
- **The "Fullness" Meter**: A circular or linear gauge showing the percentage of the current model's context window (e.g., 128k, 200k) being utilized.
- **Color Coding**:
  - `Emerald`: < 50% used.
  - `Amber`: 50% - 85% used (Threshold for warning).
  - `Red`: > 85% used (Critical - Pruning imminent).

## 2. Context Management Transparency
- **The "Pruning" Event**: When the agent summarizes or discards older context to make room, the UI displays a specialized "Memory Consolidation" card in the [Decision Trace](./REASONING_VISUALIZATION.md).
- **Discarded Data Visualization**: Allow users to click a "Discarded" icon to see which older trace entries or artifact snippets have been removed from the active context window.

## 3. Summarization UI
- **Context Snapshots**: Show the "Condensed" version of the history that the agent is currently using.
- **Human-Directed Pruning**: An advanced control where an operator can manually "Pin" a specific artifact or reasoning block to ensure it is never summarized or pruned, regardless of context pressure.

## 4. Multi-model Context Handoff
- **Window Scaling**: When switching between models with different context sizes (e.g., Haiku to Opus), show a "Refitting Context" animation that visualizes the data being expanded or compressed for the new model.

## 5. Token Efficiency Tips
- **Proactive Suggestions**: "This task is using a lot of context. Should I summarize the initial research to save tokens?"
- **Cost Impact**: Show how context length is contributing to the per-step USD spend.
