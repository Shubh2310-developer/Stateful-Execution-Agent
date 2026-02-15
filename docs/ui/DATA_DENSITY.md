# Antigravity Data Density Guidelines

As an operational tool for managing autonomous agents, Antigravity often needs to display large amounts of complex data (logs, traces, state trees, and artifacts). This document defines how we manage information density to ensure clarity without sacrificing depth.

## 1. Information Hierarchy

We use a "Progressive Disclosure" strategy:
- **Level 1: The Pulse (Low Density)**: High-level status indicators (Running/Success/Error) and progress bars. Visible at all times.
- **Level 2: The Summary (Medium Density)**: Step actions, artifact previews, and confidence scores. Accessible via cards or list items.
- **Level 3: The Deep Dive (High Density)**: Full decision traces, raw LLM reasoning, dependency graphs, and JSON state versions. Accessible via expansion or dedicated panels.

## 2. Grid & Spacing Systems

- **Base Unit**: 4px (`0.25rem`).
- **Standard Padding**: `p-4` (16px) or `p-6` (24px) for primary containers to provide "visual breathing room."
- **Compact Views**: Use `p-2` (8px) and `text-sm` for sidebar items, metadata lists, and secondary navigation to maximize vertical space.

## 3. Visual Grouping Patterns

- **Borders over Backgrounds**: Use `1px` borders (`border-slate-200`) to separate items. Avoid alternating background colors (zebra striping) which can look cluttered in high-density views.
- **Semantic Grouping**: Group related metadata (e.g., Token Usage + Latency + Model ID) into small, horizontal badges or "metadata clusters."
- **Muted Metadata**: Use lower-contrast colors (`text-slate-500`) for secondary information like timestamps or IDs to keep the focus on primary labels.

## 4. Typography for Data

- **Fixed-Width (Monospace)**: Use for IDs, code snippets, and raw log entries. Optimized for alignment and scanning.
- **Tabular Numerals**: Use `font-variant-numeric: tabular-nums` for all metrics and timestamps to ensure numbers align vertically in tables.
- **Line Length**: Limit text-heavy reasoning blocks to `max-w-prose` (~65-75 characters) to ensure readability.

## 5. View Modes

Allow the user to toggle between density modes:
- **Comfortable**: Default view with ample whitespace.
- **Compact**: Reduced padding and font sizes for "Power User" monitoring on smaller screens or complex tasks.

## 6. Scroll Management

- **Sticky Headers**: Ensure table headers and panel titles remain visible during long scrolls.
- **Sub-panel Scrolling**: Avoid global page scrolls where possible. Use independent scroll containers for the Trace panel and the Main Workplace to keep the context visible.
