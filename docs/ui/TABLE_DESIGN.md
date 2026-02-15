# Antigravity Table & Grid UX

Precision data management is a core requirement for Antigravity operators. This document defines the standards for high-density tables and data grids.

## 1. Table Visual Style
- **Borders**: Use horizontal borders only (`border-b border-slate-200`) to maintain vertical flow.
- **Background**: White surface (`bg-white`) with a very subtle hover state (`hover:bg-slate-50`).
- **Alignment**:
  - Text: Left-aligned.
  - Numbers/Metrics: Right-aligned (using [Tabular Numerals](./DATA_DENSITY.md)).
  - Status Pills: Centered or Left-aligned based on column width.

## 2. Interactive Features
- **Sorting**: Clickable column headers with sort direction indicators (Up/Down arrows).
- **Filtering**: Inline column filters or a global "Filter Bar" for complex datasets.
- **Sticky Headers**: The header row must remain pinned to the top during vertical scrolling.
- **Pagination vs. Infinite Scroll**:
  - Use **Infinite Scroll** (with virtualization) for the Decision Trace.
  - Use **Pagination** for Task History and Audit Logs to allow for precise bookmarking.

## 3. High-Density Patterns
- **Cell Truncation**: Use `text-ellipsis` for long IDs or descriptions, with a tooltip showing the full value on hover.
- **Compact Mode**: A toggle to reduce row height and font size for "Power User" data auditing.
- **Metadata Clusters**: Group related small values (e.g., `Tokens`, `Cost`, `Latency`) into a single "Metrics" column to save horizontal space.

## 4. Selection & Bulk Actions
- **Checkbox Selection**: Row-level checkboxes for bulk actions (e.g., "Archive 10 Tasks").
- **Action Bar**: A floating bottom bar that appears when one or more rows are selected, showing available bulk operations.
- **Single-row Actions**: A "More" icon (`EllipsisVertical`) at the end of each row for context-specific actions (e.g., "Download PDF," "View State").

## 5. Performance
- **Virtualization**: Mandatory for tables exceeding 100 rows.
- **Skeleton Loading**: Render table shell and skeleton rows while data is fetching to prevent layout shift.
- **Memoized Rows**: Prevent re-rendering of the entire table when a single row's status updates.
