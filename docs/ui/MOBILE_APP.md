# Antigravity Mobile App Experience

While the primary operational environment for Antigravity is the desktop, the mobile experience is critical for "on-the-go" monitoring and urgent interventions. This document defines the native-like patterns for the Antigravity mobile app.

## 1. The "Mission Summary" Dashboard

- **Focus**: High-level status and critical alerts.
- **Layout**: A vertical list of "Actionable Tasks" showing Goal Title, Status Pill, and a Sparkline of recent activity.
- **Primary Action**: A prominent "Create Task" button (FAB) at the bottom right.

## 2. Mobile Monitoring UX

- **The "Pulse" View**: A simplified version of Mission Control.
- **Condensed Trace**: Only show "High-Impact" or "Error" entries by default. Allow the user to "Tap to Expand" the full log.
- **Live Notifications**: Push notifications for task completion, checkpoint requests, or critical failures.

## 3. Interaction Patterns (Touch-First)

- **Haptic Feedback**: Subtle vibrations for task milestones and error states.
- **Gestures**:
  - `Swipe Right` to approve a checkpoint.
  - `Swipe Left` to pause or cancel a task.
  - `Pull to Refresh` for a global sync.
- **Bottom Sheets**: Use for complex inputs like "Refinement Requests" or "Memory Management."

## 4. Optimized Visuals

- **High Contrast**: Ensure readability in outdoor/bright environments.
- **Typography**: Increase body font size to `16px` minimum.
- **Icon-Heavy**: Use icons to save horizontal space while maintaining clarity.

## 5. Offline & Low-Bandwidth States

- **Optimistic Sync**: Cache the latest state locally to allow "Instant Open" even with poor connectivity.
- **Data Saver Mode**: Defer the loading of large artifacts and complex graphs until on a Wi-Fi connection.
- **Local Persistence**: Save "Draft Feedback" locally if the connection drops, and sync automatically when back online.
