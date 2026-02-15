# Antigravity UI Interactions & Motion

This document defines the behavioral patterns and micro-interactions for the Antigravity UI. We prioritize functional feedback over decorative animation.

## 1. Interaction Principles

- **Response Latency**: Interactions must feel instantaneous (< 100ms).
- **Physical Plausibility**: Motion should feel weighted and deliberate, avoiding "bouncy" or excessive easing.
- **Intentional Feedback**: Every user action (and agent action) must be acknowledged visually.

## 2. Agent Status Transitions

Since the agent is autonomous, the UI must signal state changes without requiring manual refresh.

- **Status Pills**: Use `animate-pulse` for "Running" states. Transition to a solid state with a subtle color flash (Emerald for Success, Red for Error) when the task completes.
- **Progress Bars**: Smooth linear transitions for task progress. If a task stalls, the progress bar should "shimmer" to indicate the system is still active but waiting (e.g., API timeout).

## 3. Micro-Interactions

### Hover States
- **Cards**: Shift border color from `slate-200` to `blue-400` and apply a very subtle Y-axis lift (`-2px`).
- **Buttons**: Shift background color by 10% (e.g., `blue-600` to `blue-700`).
- **Icons**: Increase opacity from `0.6` to `1.0`.

### Navigation
- **Sidebar**: Active links use a left-border accent (`border-l-4 border-blue-600`) and a subtle background highlight.
- **Panels**: The Trace Panel should slide in from the right with an `ease-out` transition over `250ms`.

## 4. Feedback Loops

- **Toasts**: Non-disruptive notifications for artifact generation or task updates. Bottom-right placement.
- **Empty States**: Use high-quality SVG illustrations (e.g., Lucide icons) to guide users when no tasks are active.
- **Skeleton Screens**: Use skeleton loaders for initial page loads to reduce perceived latency and prevent layout shift.

## 5. Decision Trace Motion

- **Auto-scroll**: The Decision Trace panel should auto-scroll as new entries arrive, but pause if the user manually scrolls up to inspect a previous decision.
- **Expansion**: When a user clicks a decision to "Deep Dive," the entry should expand accordion-style with a smooth height transition.
