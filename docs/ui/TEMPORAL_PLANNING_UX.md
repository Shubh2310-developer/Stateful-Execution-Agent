# Antigravity Temporal Planning & Scheduling UX

Autonomous agents are most effective when they manage time, recurrence, and future intent. This document defines the UI patterns for temporal mission management.

## 1. The Mission Calendar
- **Layout**: A standard daily/weekly/monthly grid view showing when missions are scheduled to run.
- **Time-blocking**: Visual blocks showing the predicted duration of each task, helping to identify "Agent Congestion."

## 2. Recurring Mission UI
- **Recurrence Editor**: A simple interface for setting patterns (e.g., "Every Monday at 9:00 AM" or "Every time the revenue dashboard updates").
- **Blueprint Sync**: (See [TASK_TEMPLATE_UX.md](./TASK_TEMPLATE_UX.md)) - Linking a schedule to a specific, verified mission plan.

## 3. The "Future Trace"
- **Anticipatory Planning**: The agent generates a plan for a future task and allows the user to "Pre-approve" it or set "Conditional Triggers."
- **Visual Style**: Muted, translucent "Future Nodes" on the state graph that turn solid when execution begins.

## 4. Time-based Triggers
- **Event Listeners**: A UI to configure external triggers (e.g., "Run research mission when a competitor releases a new feature").
- **Delay Controls**: A "Pause Until" button to defer execution to a specific time or event.

## 5. Historical vs. Future Analysis
- **Temporal ROI**: A chart showing value saved "To-date" vs. "Projected Savings" from scheduled recurring tasks.
- **Trend Extrapolation**: The agent suggests future tasks based on patterns in historical data (e.g., "I've noticed a monthly spike in churn; should I schedule a retention analysis for next month?").
