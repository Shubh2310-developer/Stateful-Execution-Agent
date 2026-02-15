# Antigravity Stateful Session UX

Persistence is the "S" in Antigravity (Stateful). This document defines how the UI handles session continuity, cross-device resumption, and state preservation.

## 1. Session Persistence Principle
- **Infinite Sessions**: Unless explicitly signed out, a user's session remains active.
- **State-by-ID**: Every mission goal has a unique, permanent URL. Re-opening this URL restores the exact state of the Workplace, Trace, and Graph.
- **Draft Preservation**: Any unsaved user input (e.g., feedback drafts, new task goals) is cached locally and synced to the backend to prevent data loss.

## 2. Cross-device Handoff
- **Active Task Sync**: If a user is monitoring a task on Desktop and opens the Mobile app, they receive a "Pick up where you left off" prompt.
- **Live State Transfer**: Real-time WebSocket sync ensures that an approval given on Mobile is instantly reflected on the Desktop view.
- **QR Code Handoff**: A "Mobile Link" button in the Desktop header generates a QR code to quickly open the current task on a mobile device.

## 3. Resumption Contextualization
When a user returns to a session after an absence:
- **"While You Were Away"**: A specialized modal or banner summarizing agent activity during the offline period.
- **Decision Highlights**: The agent points out the top 3 most important decisions it made autonomously while the user was gone.
- **Artifact Diff**: A visual indicator showing what has been added or modified in the Workplace since the user's last activity.

## 4. Multi-tab Synchronization
- **Cross-tab Messaging**: Using BroadcastChannel API to ensure that if a user changes a global setting (e.g., Theme, Mute Notifications) in one tab, it propagates to all open Antigravity tabs instantly.
- **Active Tab Detection**: The "Pulse" animation and real-time trace only active in the focused tab to save system resources, while other tabs remain in a "Passive Sync" state.

## 5. Session Expiry & Security
- **Graceful Timeouts**: Before a session expires due to security policy, the UI shows a "Session Expiring" countdown with a "Stay Signed In" button.
- **Secure Re-auth**: If the user needs to re-authenticate, the UI preserves the background task state so the user can return to exactly where they were after logging back in.
