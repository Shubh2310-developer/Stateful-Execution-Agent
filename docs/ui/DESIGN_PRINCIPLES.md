# Antigravity UI Design Principles

These principles guide every design decision for the Antigravity UI, ensuring it remains an effective tool for managing autonomous AI.

## 1. Transparency over Mystery (The Glass Box)
The user should never have to guess what the agent is doing or why.
- **Application**: The Decision Trace is always accessible. Reasoning is never hidden behind a generic "Loading" state.

## 2. Agency over Automation
The agent works for the user, not the other way around.
- **Application**: High-impact actions always require confirmation. The user can pause or cancel a task at any time.

## 3. Density with Clarity
Operators need a lot of information, but they shouldn't be overwhelmed.
- **Application**: Use [Progressive Disclosure](./DATA_DENSITY.md) to hide complexity until it is requested. Use consistent grids to organize high-density data.

## 4. Feedback over Decoration
Every animation and visual shift must serve a functional purpose.
- **Application**: A pulsing status indicates activity; a red border indicates an error. If an element isn't communicating state or directing action, simplify it.

## 5. Accessibility as a Default
An enterprise tool is only useful if everyone can use it.
- **Application**: Design for keyboard navigation and high contrast from the start. Follow the [Accessibility Checklist](./ACCESSIBILITY_CHECKLIST.md).

## 6. Persistence & Contextual Awareness
The UI should "Remember" just like the agent does.
- **Application**: Layout preferences, collapsed panels, and search filters should persist across sessions.

## 7. Professional Reliability
The interface should feel stable and high-performance.
- **Application**: Use a polished Flat Design style. Prioritize fast interaction times and stable layouts (0 CLS).
