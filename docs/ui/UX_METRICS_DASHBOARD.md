# Antigravity UX Metrics Dashboard

To ensure the agentic interface remains high-performance and user-friendly, we monitor specialized UX metrics. This document defines the tracking patterns for product health.

## 1. Efficiency Metrics
- **Time to Goal Initiation**: How long it takes from opening the dashboard to starting a mission.
- **Correction Frequency**: The ratio of tasks that require human intervention vs. those that run autonomously to completion.
- **Shortcut Usage**: Percentage of actions taken via the [Command Palette](./COMMAND_PALETTE.md) vs. mouse clicks.

## 2. Quality & Satisfaction
- **CSAT (Customer Satisfaction Score)**: Aggregated 1-5 star ratings from the [Feedback System](./FEEDBACK_SYSTEM.md).
- **Learning Retention**: Metric showing if a user has to correct the agent for the same mistake more than once.
- **Success Rate Trend**: Monitoring the improvement of organizational task success over time.

## 3. Client Performance (Web Vitals)
- **Trace Latency**: Real-time monitoring of how long it takes for a decision to appear in the UI after it happens in the backend.
- **Graph Render Time**: Performance monitoring for complex [State Visualizations](./STATE_VISUALIZATION.md).
- **Lighthouse Score Tracking**: Historical trend of accessibility and performance scores.

## 4. Behavioral Heatmaps
- **Decision Trace Hotspots**: Visualizing which parts of the reasoning log users spend the most time reading.
- **Artifact Interaction**: Tracking how often users download, share, or refine generated artifacts.

## 5. Multi-device Mix
- **Session Continuity**: How often tasks are started on desktop and monitored/completed on mobile.
- **Breakpoint Success**: Tracking error rates per device type to identify responsive UI issues.
