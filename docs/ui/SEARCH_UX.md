# Antigravity Search & Discovery UX

Search is the primary way operators find historical context, specific artifacts, and learned patterns. This document defines the UX standards for search and discovery.

## 1. Global Search Pattern
- **Access**: Persistent search bar in the header and the [Command Palette](./COMMAND_PALETTE.md).
- **Scope**: Federated search across Tasks, Artifacts, Memory, and System Logs.
- **Results**: Real-time, fuzzy-matched results grouped by category.

## 2. Advanced Filtering
For high-density views like the Task History:
- **Facet Search**: Sidebar filters for Date Range, Goal Category, Tool Usage, and Satisfaction Score.
- **Query Language**: Support for simple boolean operators (e.g., `"investor update" AND 2024`).
- **Filter Chips**: Dynamic chips that can be clicked to remove specific constraints.

## 3. Search Result Highlighting
- **Contextual Snippets**: Show the part of the artifact or trace entry that matched the query, with the keywords highlighted (`bg-blue-100`).
- **Relevance Ranking**: Prioritize "Active" tasks and "High Confidence" memory entries.

## 4. Discovery & Recommendations
Proactive search results based on user context.
- **"Similar to This"**: When viewing a task, show a sidebar with 3 similar historical tasks.
- **Knowledge Discovery**: A "Did you know?" widget in the Memory view that surfaces under-utilized learned patterns.

## 5. Visual Feedback
- **Zero Results**: Guide the user to broaden their search (see [Error & Empty States](./ERROR_STATES.md)).
- **Shimmer Loading**: Use skeleton loaders for search result items to maintain layout stability.
