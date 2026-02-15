# Antigravity UI Performance Targets

Performance in the Antigravity UI is about more than just speed; it's about maintaining a synchronous "Heartbeat" between the autonomous agent and the operator. This document defines our client-side performance goals for 2026.

## 1. Interaction Latency (The 100ms Rule)

Every user action must result in a visual change within **100ms**.
- **Button Clicks**: Immediate hover/active state transition.
- **Navigation**: Instantaneous page swaps (utilizing Client-Side Routing and Prefetching).
- **Expansion**: Accordion/Trace expansion animations must begin immediately.

## 2. Load Performance (Core Web Vitals)

- **LCP (Largest Contentful Paint)**: < 1.2s. The primary Dashboard grid must be visible almost instantly.
- **FID (First Input Delay)**: < 50ms. The UI must be interactive as soon as it's visible.
- **CLS (Cumulative Layout Shift)**: 0.0. Use skeleton screens and fixed-size containers to prevent content jumping during async data loads.

## 3. Real-time Sync (The "Heartbeat")

The agent's decision trace must sync with the UI with minimal lag.
- **Trace Latency**: < 200ms from the event being logged in the backend to it appearing in the UI.
- **WebSocket/SSE Performance**: Maintain a stable, low-overhead connection for real-time updates. Use message batching if the agent is producing more than 10 trace entries per second.

## 4. Rendering Efficiency

- **Virtualization**: Use list virtualization (e.g., `react-window`) for long Decision Traces. We expect some tasks to generate thousands of entries.
- **Memoization**: Aggressively use `React.memo` or equivalent to prevent unnecessary re-renders of complex components (like the State DAG) when only the Trace Panel updates.
- **Asset Optimization**: All icons (SVG) and illustrations must be inlined or cached to prevent flickering.

## 5. Perceived Performance Patterns

- **Skeleton Screens**: Use for the Dashboard grid and Artifact previews.
- **Optimistic UI Updates**: When a user provides feedback or "Accepts" a step, update the UI state immediately before the API confirmation arrives.
- **Streaming UI**: For Markdown artifacts, render the text as it arrives (streaming) rather than waiting for the complete block.

## 6. Resource Limits

- **Bundle Size**: Initial JS bundle < 150KB (gzipped). Use code-splitting for specialized views (e.g., the State Visualization canvas).
- **Memory Usage**: The client should not exceed 200MB of RAM, even with a long-running task active. Perform garbage collection on older trace entries if they exceed a certain threshold (keeping them available via "Load More").
