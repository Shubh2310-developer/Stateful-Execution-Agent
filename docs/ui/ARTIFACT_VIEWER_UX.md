# Antigravity Artifact Viewer UX

The Artifact Viewer is the primary workspace where users interact with the agent's output. This document defines the rendering and interaction patterns for different artifact types.

## 1. Universal Viewer Features
- **Full-screen Toggle**: Allow the viewer to expand to fill the entire browser window.
- **Download/Export Bar**: Persistent header with buttons for `Download`, `Copy to Clipboard`, and `Send to Integration`.
- **Version Selector**: Access to the [Time Travel](./VERSIONING_UX.md) history for the specific artifact.

## 2. Document Rendering (Markdown/PDF)
- **Streaming Render**: For Markdown, render the structure (headers, lists) in real-time as the agent "writes" the content.
- **Interactive TOC**: A side-panel Table of Contents that allows for quick navigation within long documents.
- **Annotation Layer**: Allow users to highlight text and leave "Refinement" comments directly on the document.

## 3. Data Rendering (JSON/CSV/Table)
- **Grid View**: Render structured data as a high-performance [Table](./TABLE_DESIGN.md).
- **JSON Tree**: For technical artifacts, provide an expandable/collapsible tree view with syntax highlighting.
- **Search within Artifact**: A local search bar to find specific values or keys within the data.

## 4. Media Rendering (Charts/Images)
- **Dynamic Charts**: Render JSON-based chart specs using [Data Visualization Patterns](./DATA_VIS_PATTERNS.md).
- **Zoom & Pan**: For high-resolution images or complex graphs, provide standard zoom/pan controls.
- **Image Comparison**: A slider to compare "Before" and "After" image artifacts during a refinement loop.

## 5. Implementation (The "Workplace" Center)
The Artifact Viewer lives in the center of the **Mission Control** layout.
- **Empty State**: Show a minimalist placeholder while the agent is planning or in the first step of execution.
- **Loading Transition**: Use a subtle fade-in transition when switching between different artifact types (e.g., moving from a Table to a Chart).
