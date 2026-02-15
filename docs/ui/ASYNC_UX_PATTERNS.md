# Antigravity Async UX Patterns

As an autonomous worker, Antigravity often performs tasks that take minutes or hours. This document defines how we maintain user engagement and visibility during asynchronous execution.

## 1. The "Pulse" of Autonomy
- **Activity Shimmer**: A subtle, non-distracting animation in the task card that signals "Work in Progress."
- **Step-level Progress**: Don't just show total progress; show the status of the *current* step (e.g., "Step 3: Analyzing 45% complete").
- **Time-to-Completion Forecast**: A dynamic estimate based on historical performance for similar tasks.

## 2. Background Task Visibility
- **The "Minimap"**: A small, floating task list in the corner of the dashboard that shows all background tasks at a glance.
- **Handoff Notifications**: Use the [Notification Strategy](./NOTIFICATIONS.md) to bring the user back only when they are needed.
- **Live Stream Preview**: A tiny, scrollable window into the Decision Trace so the user can "Peep" into the agent's thinking without leaving their current view.

## 3. Resumption UX
- **Context Restore**: When a background task completes or requires input, the UI "Reconstructs" the workspace state as it was when the task started.
- **Interruption Recovery**: If the user's connection drops, show a "Reconnecting to Active Mission..." indicator.

## 4. Perceived Performance for Long Tasks
- **Intermediate Artifacts**: Show "Draft" versions of artifacts as they are generated so the user can begin reviewing before the task is 100% finished.
- **Milestone Celebrations**: Small visual cues (e.g., a green check pulse) when a major dependency is resolved.

## 5. Goal Evolution UI
- **Intent Shifts**: If the agent discovers new information that requires it to change its plan, use a "Plan Update" animation to show how the remaining async steps have evolved.
- **Pause & Pivot**: A clear button to pause the async flow and "Redirect" the agent if the user sees it heading in the wrong direction.
