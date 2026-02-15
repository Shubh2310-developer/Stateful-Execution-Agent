# Antigravity API Documentation UX

As a developer-first platform, Antigravity's API documentation is more than just text; it is an interactive workspace for integration and testing. This document defines the UX patterns for the developer documentation.

## 1. Visual Language
- **Theme**: Dark mode by default (`bg-slate-950`), following the [Dark Mode](./DARK_MODE.md) specs.
- **Typography**: `JetBrains Mono` for all code snippets and endpoint paths.
- **Layout**: Three-column layout:
  - Left: Navigation and Search.
  - Center: Explanation and Schema details.
  - Right: Live Code Samples and "Try it Out" console.

## 2. Interactive "Try it Out" Console
Every endpoint must have a live testing interface.
- **Auth Simulation**: Allow users to enter a temporary API key or use a "Sandbox Key."
- **Request Builder**: A structured form for adding query parameters, headers, and request bodies.
- **Response Preview**: High-performance JSON viewer with syntax highlighting and a "Copy to Clipboard" button.

## 3. Schema & Type Exploration
- **Expandable Objects**: Nested JSON objects should be collapsible.
- **Type Badges**: Clearly label types (e.g., `string`, `int`, `ISO-8601`) with distinct colors.
- **Required Markers**: Use a red asterisk or a `Required` badge for mandatory parameters.

## 4. Multi-Language Code Snippets
- **Language Selector**: Tabs for `Python`, `JavaScript`, `TypeScript`, `cURL`, and `Go`.
- **SDK Sync**: Ensure code snippets reflect the latest versions of the official Antigravity SDKs.
- **One-click Copy**: A persistent copy icon on all code blocks.

## 5. Navigation & Search
- **Fuzzy Search**: A command-palette style search that jumps to specific endpoints or concepts.
- **Version Switcher**: A dropdown to switch between API versions (e.g., `v1`, `v2-beta`).
- **Deep Linking**: Every heading and endpoint must have a permanent anchor link for easy sharing.

## 6. Decision Trace API Visualization
Specialized documentation for the Trace event stream.
- **Event Schema Catalog**: A list of all possible `event_type` schemas.
- **Real-time Stream Demo**: A live, simulated socket connection showing how trace events arrive and are structured.
