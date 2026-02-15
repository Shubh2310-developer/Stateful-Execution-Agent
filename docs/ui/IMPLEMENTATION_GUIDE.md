# Antigravity UI Implementation Guide

This guide provides technical instructions for frontend developers implementing the Antigravity UI.

## 1. Recommended Tech Stack
- **Framework**: [Next.js 14+](https://nextjs.org/) (App Router)
- **Styling**: [Tailwind CSS](https://tailwindcss.com/)
- **State Management**: [Zustand](https://github.com/pmndrs/zustand) (for client state) + [React Query](https://tanstack.com/query/latest) (for server state)
- **Icons**: [Lucide React](https://lucide.dev/)
- **Visualizations**: [React Flow](https://reactflow.dev/) (for state graphs) + [Recharts](https://recharts.org/) (for metrics)
- **Real-time**: [Socket.io](https://socket.io/) or Server-Sent Events (SSE)

## 2. Component Implementation Strategy

### 2.1 The "Glass Box" Trace
Implement the Trace Panel as a virtualized list. Since traces can grow to thousands of entries per task, use `react-window` or `@tanstack/react-virtual`.

### 2.2 Shared Styling Patterns
Utilize the Tailwind configuration to enforce the Antigravity Design System.

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: '#3B82F6',
        secondary: '#60A5FA',
        cta: '#F97316',
        background: '#F8FAFC',
        surface: '#FFFFFF',
        text: '#1E293B',
      },
      fontFamily: {
        sans: ['"Plus Jakarta Sans"', 'sans-serif'],
      },
    },
  },
}
```

## 3. Real-time Synchronization

The frontend should maintain a persistent connection to the Backend API to receive trace events.

```typescript
// Example Socket.io Listener
socket.on('trace_event', (event: TraceEntry) => {
  useTaskStore.getState().addTraceEntry(event.task_id, event);
});
```

## 4. Handling State Versions

Implement a "Time Travel" selector that allows users to view the UI state at different `version_id` points. When a version is selected:
1. Fetch the state snapshot for that version.
2. Update the `useTaskStore` with the historical state.
3. Disable all "destructive" actions (edit/delete) while viewing history.

## 5. Deployment & Optimization

- **Build Pipeline**: Ensure SVGs are optimized via `svgo-loader`.
- **Lighthouse Goals**: Aim for 95+ scores in Performance, Accessibility, and Best Practices.
- **Error Boundaries**: Implement granular error boundaries at the component level (e.g., if the State Graph fails to render, the Trace Panel should still function).
