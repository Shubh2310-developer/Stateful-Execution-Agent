# Antigravity Multi-modal Artifact Patterns

Antigravity creates complex, multi-modal artifacts that combine text, structured data, and visualizations. This document defines the patterns for handling these integrated outputs.

## 1. Integrated Document Pattern
The most common artifact type, combining various media into a cohesive narrative.
- **Markdown Core**: The primary structure is Markdown-based text.
- **Embedded Components**:
  - **Inline Charts**: Interactive Recharts components embedded directly in the document flow.
  - **Data Tables**: High-density tables with sorting and filtering capability.
  - **Media Previews**: Thumbnails for generated images or external links.

## 2. The "Dashboard" Artifact
A specialized artifact that serves as a real-time reporting surface.
- **Grid Layout**: A collection of widgets (metrics, charts, logs) arranged for quick situational awareness.
- **Live Updating**: The artifact itself can update if the underlying data sources change (optional based on goal).
- **Export to PDF**: A "Flattened" version of the dashboard for static sharing.

## 3. Code & Technical Packages
Artifacts consisting of multiple files and technical specifications.
- **File Explorer**: A sidebar allowing navigation through a multi-file generated artifact (e.g., a code refactor).
- **Dependency Map**: A visualization of how the generated files relate to each other.
- **Test Results**: Integrated view showing the pass/fail status of any generated tests.

## 4. Visual Navigation within Multi-modal Artifacts
- **Anchored Reasoning**: Specific sections of the artifact are linked to the [Decision Trace](./REASONING_VISUALIZATION.md) entry that justified their creation.
- **Source Citations**: Hover over a data point to see the raw source (e.g., "Source: Customer Support Slack Channel").

## 5. Refinement of Multi-modal Content
- **Component-Level Feedback**: Users can click a specific chart or table within a document and request a refinement just for that element (e.g., "Change this chart to a bar graph").
- **Atomic Rollback**: Revert a specific component of a multi-modal artifact to a previous version without affecting the rest of the document.

## 6. Storage & Export Standards
- **Unified Package**: Multi-modal artifacts are stored as a versioned "Artifact Package" containing all raw data, assets, and the final rendered view.
- **Smart Export**: When exporting to PDF, the system automatically converts interactive charts into high-resolution static images.
