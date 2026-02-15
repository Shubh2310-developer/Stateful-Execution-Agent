# Antigravity Cross-platform Continuity UX

Antigravity provides a seamless "Mission Continuity" experience as users move between Web, CLI, Mobile, and VR. This document defines the handoff patterns.

## 1. Universal Task ID
- Every mission has a unique, cross-platform identifier (e.g., `mission-alpha-9`).
- **Deep Linking**: Links to missions work across all platforms (e.g., opening a Slack link on Mobile launches the App; on Desktop it launches the Web UI).

## 2. Handoff Scenarios
- **CLI to Web**: A developer initiates a task via the terminal and uses the `open` command to view the live State Graph in the browser.
- **Web to Mobile**: A user starts a task at their desk and "Follows" it on their phone while walking to a meeting.
- **Mobile to VR**: An operator receives an alert on their phone and puts on a headset to enter the [VR Workspace](./VR_WORKSPACE_UX.md) for deep swarm debugging.

## 3. State Preservation (The "Frozen" UI)
- When switching platforms, the UI state (expanded panels, scroll position, filters) is synced to the backend so the user finds the exact same workspace on the new device.
- **Handoff Notification**: "You were just viewing this task on Desktop. Would you like to resume here?"

## 4. Capabilities by Platform
The UI intelligently adapts based on what the current device can do:
- **CLI**: Optimized for high-speed commands and raw data.
- **Web**: Full-featured mission control and data visualization.
- **Mobile**: Focused on status, alerts, and simple approvals.
- **VR/Spatial**: Focused on swarm coordination and 3D graphs.

## 5. Continuity Pulse
- **Cross-platform Presence**: If a user is active on two devices simultaneously, the UI shows a "Multi-session" indicator in the header.
- **Sync Heartbeat**: A subtle visual cue that ensures the user the state is "Live" across all endpoints.
