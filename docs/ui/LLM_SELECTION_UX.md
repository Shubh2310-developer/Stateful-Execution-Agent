# Antigravity LLM Selection UX

Antigravity is model-agnostic. This document defines the patterns for choosing and switching between different Large Language Models (LLMs).

## 1. Selection during Planning
- **Model Recommendation**: The agent suggests the optimal model for a goal based on complexity.
  - *Fast Mode*: Uses Haiku 4.5 or similar for low-complexity, high-speed tasks.
  - *Balanced Mode*: Uses Sonnet 4.5 for standard knowledge work.
  - *High-Precision Mode*: Uses Opus 4.6 for complex reasoning or code.
- **Manual Overrides**: Users can click the "Model" badge to select a specific provider or model version manually.

## 2. Dynamic Model Switching
- **Step-level Selection**: Allow the planner to assign different models to different steps in a single plan (e.g., Haiku for search, Opus for synthesis).
- **Auto-escalation UI**: If a model fails to meet success criteria twice, the UI suggests: "This task seems complex. Should I try a more powerful model?"

## 3. Cost & Performance Transparency
- **Price Indicators**: Clearly show the estimated cost per 1k tokens for the selected model.
- **Speed Benchmarks**: A small "Latency Gauge" showing the average response time for the selected model.
- **Capability Badges**: Icons indicating specialized strengths (e.g., `Coding`, `Long Context`, `Low Latency`).

## 4. Provider Status & Health
- **Provider Multi-tenancy**: Allow users to connect multiple API keys (Groq, Anthropic, OpenAI).
- **Fallback Visualization**: If the primary provider is down, show a "Failing over to [Provider B]" status message.

## 5. Specialized "Swarms" (Multi-agent)
- **Agent Attribution**: (See [MULTI_AGENT_UX.md](./MULTI_AGENT_UX.md)) - Show which model is "Powering" each specialized agent in the swarm.
- **Instruction Tuning**: A direct link from the model selector to the [Prompt Editor](./PROMPT_EDITOR_UX.md) to customize the model's behavior.
