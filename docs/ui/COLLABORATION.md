# Antigravity Collaboration UX

In enterprise environments, multiple users often monitor, review, or contribute to the same agentic tasks. This document defines the UX patterns for multi-user collaboration in Antigravity.

## 1. Shared Situational Awareness

- **Live Presence**: Show who is currently viewing a task (e.g., small user avatars in the header).
- **Synchronized State**: All connected users see the same real-time "Pulse" and "Decision Trace."
- **Activity Feed**: A secondary log showing "Who did what" (e.g., "User A approved Step 3," "User B refined the summary").

## 2. Collaborative Decision Making

When a task hits a "Human-in-the-Loop" checkpoint:
- **Approval Queue**: Multiple authorized users can review the same checkpoint.
- **Commenting**: Users can leave "Operator Notes" on specific trace entries to explain their reasoning to other team members.
- **Multi-user Approval**: Configurable rules for high-impact actions (e.g., "Requires 2/3 approvals before sending the email").

## 3. Role-Based Access Control (RBAC) UX

- **Permission Badges**: Clearly show the user's current role (e.g., "Viewer," "Operator," "Admin") and what actions are restricted.
- **Action Ghosting**: Disable buttons or inputs that the current user is not authorized to use, with a tooltip explaining why.
- **Shared Memory**: Differentiate between "Private Preferences" (specific to a user) and "Team Patterns" (learned from the entire organization).

## 4. Notification & Handoff

- **Task Assignments**: Assign an active task to a specific operator for oversight.
- **Handoff Toasts**: Notify the team when a task changes hands or requires attention from a different role.
- **Mentions**: Support `@user` mentions in feedback and comments to trigger platform-specific notifications (Slack/Email).

## 5. Security in Collaboration

- **Audit Logs**: Every collaborative action is recorded in the permanent audit log.
- **Session Isolation**: Ensure that while the task is shared, sensitive user-specific data (like individual API keys) is never leaked between team members.
