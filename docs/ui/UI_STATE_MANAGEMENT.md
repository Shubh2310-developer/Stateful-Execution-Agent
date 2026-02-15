# Antigravity UI State Management Patterns

Managing the complex, real-time UI state of a stateful agent requires a robust architecture. This document defines our frontend state management strategy.

## 1. State Categorization
- **Server State**: Task data, artifacts, memory, and logs (Managed by `TanStack Query`).
- **UI State**: Sidebar visibility, panel widths, active tab, and filter settings (Managed by `Zustand`).
- **Real-time State**: Streaming trace events and progress pulses (Managed by `WebSockets/Socket.io`).
- **Form State**: Goal input and refinement drafts (Managed by `React Hook Form`).

## 2. The "Single Source of Truth" Rule
- The **Version ID** of the task state is the primary key for the entire UI.
- All components must react to changes in the version ID, ensuring that the Workplace, Trace, and Graph are always in sync.

## 3. Real-time Event Handling
- **The Event Buffer**: Incoming trace events are buffered and added to the UI in batches (e.g., every 100ms) to prevent UI thrashing during high-speed reasoning.
- **Optimistic Updates**: When a user clicks "Approve," the UI transitions to the "Success" state immediately while the API request is in flight.

## 4. Persistence of UI Preferences
- Use `localStorage` or a specialized "UI Settings" DB table to persist:
  - Theme (Light/Dark/Spatial).
  - Column widths in the Task History table.
  - Collapsed/Expanded states of the Decision Trace entries.

## 5. State Debugging Surface
- **The "State Inspector"**: A hidden (Dev-only) panel that shows the raw JSON of the current `Zustand` stores and the active `Query` cache.
- **Action Log**: A console-like view of all UI-triggered actions (e.g., `TOGGLE_SIDEBAR`, `SELECT_TASK`).

## 6. Error Boundaries & Recovery
- **Component Isolation**: If a complex visualization (like the 3D State Graph) crashes, it should be caught by an Error Boundary, showing a "Visualization Unavailable" message while keeping the rest of the dashboard functional.
- **State Reset**: A "Nuclear Option" in settings to clear all local UI state and reload from the server.
