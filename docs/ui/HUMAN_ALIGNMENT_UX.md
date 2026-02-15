# Antigravity Human Alignment UX Patterns

Human Alignment ensures the agent's intents and ethical boundaries match the user's requirements. This document defines the patterns for intent tracking and ethics monitoring.

## 1. Intent Verification UI
- **Goal Alignment Gauge**: A real-time score showing how closely the current execution plan matches the user's high-level goal.
- **Constraint Checklist**: A persistent list in the workplace showing all user-imposed constraints (e.g., "No external APIs," "Technical tone") and their status.

## 2. Ethics & Policy Trace
- **Safety Heuristics**: Specialized entries in the Decision Trace when the agent weighs an action against safety or privacy policies.
- **Policy Violations**: Red-line indicators if an agent-proposed action conflicts with an organizational guardrail.

## 3. Value-based Decision Making
- **Rationale for "Why"**: The agent explains its choices in terms of user-defined values.
  - *Example*: "I selected Model B because you prioritize 'Cost Efficiency' over 'Extreme Speed' in your settings."

## 4. Bias & Diversity Indicators
- **Source Diversity**: For research tasks, a visualization showing the variety of data sources used (e.g., geographical spread, viewpoint diversity).
- **Bias Alerts**: Muted warnings if the agent detects it is relying too heavily on a single perspective or dataset.

## 5. Alignment Feedback Loops
- **"Not what I meant" Control**: A high-speed button in the trace that pauses execution and allows the user to re-state their intent.
- **Intent Refinement**: The agent asks clarifying questions about "Why" a goal is important to better align its tactical choices.
