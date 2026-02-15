# Antigravity Dashboard Widgets

The Antigravity Dashboard is composed of modular, data-rich widgets that provide immediate ROI and operational visibility. This document defines the primary widget types.

## 1. ROI & Impact Widgets
- **Time Saved Counter**: A large, numerical display showing the cumulative hours saved by the agent across all tasks.
- **Goal Completion Rate**: A donut chart showing the percentage of tasks that reached "Completed" vs. those requiring manual intervention.
- **Mission Velocity**: A line chart showing the trend of "Goals Met per Week."

## 2. Resource & Cost Widgets
- **Real-time Burn Rate**: A speedometer-style gauge showing the current USD spend per hour based on active task token usage.
- **Model Distribution**: A pie chart showing the breakdown of usage between different LLM models (e.g., Sonnet 4.5, Haiku 4.5).
- **API Health Matrix**: A grid of status indicators for all connected tools and external APIs.

## 3. Task Monitoring Widgets
- **Active Task Pulse**: A high-density list showing the top 5 running tasks with their current step and progress shimmer.
- **Recent Artifacts Carousel**: A horizontal scroll of the latest 10 generated documents/reports with one-click previews.
- **Human-in-the-Loop Queue**: A red badge indicator showing how many tasks are currently paused awaiting user input.

## 4. Learning & Memory Widgets
- **New Facts Learned**: A count of memory entries added in the last 24 hours.
- **Preference Impact**: A summary showing which learned preference (e.g., "Concise tone") was most frequently used recently.
- **Memory Strength Heatmap**: A visualization of which "Domain Clusters" in memory are most robust.

## 5. Implementation Rules
- **Refresh Interval**: Widgets should refresh their data every 30 seconds unless they are "Real-time" (which use WebSockets).
- **Interactivity**: Every widget must be clickable, taking the user to the corresponding deep-dive view (e.g., clicking the Cost widget opens `ANALYTICS_UX`).
- **Customization**: Allow users to drag-and-drop, resize, and remove widgets from their personal dashboard.
