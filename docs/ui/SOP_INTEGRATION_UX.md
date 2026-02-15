# Antigravity SOP Integration UX

Standard Operating Procedures (SOPs) are the guardrails for professional knowledge work. Antigravity integrates SOPs into the agent's planning and execution. This document defines the UI patterns for SOP visualization and compliance.

## 1. SOP Library Interface
- **Procedure Browser**: A searchable directory of organizational SOPs.
- **Step-by-step View**: Rendering of the SOP as a clear, numbered checklist with associated criteria.
- **Integration Points**: Clearly mark which steps in an SOP can be handled by the agent vs. which require a human.

## 2. Planning with SOPs
- **Template Matching**: When a user enters a goal, the agent proactively suggests relevant SOPs (e.g., "This goal matches our 'Quarterly Audit' procedure. Should I follow that SOP?").
- **Automatic Step Generation**: The agent populates its plan directly from the SOP steps, ensuring 100% compliance with organizational standards.

## 3. SOP Compliance in the Trace
- **Compliance Badges**: Every entry in the Decision Trace is linked to a specific SOP step.
- **Deviation Alerts**: If the agent needs to deviate from the SOP (e.g., a tool is unavailable), the UI flags this as a high-priority "Compliance Warning" in the trace.
- **Evidence Collection**: The agent automatically captures artifacts (screenshots, logs) required by the SOP for audit purposes.

## 4. SOP Creation & Editing
- **Agent-assisted SOP Generation**: After a successful custom task, the agent suggests: "Would you like to save this successful execution path as a new SOP?"
- **Interactive Builder**: A drag-and-drop interface for defining steps, success criteria, and required tools for a new procedure.

## 5. Analytics for Procedures
- **SOP Efficiency**: Metrics showing which procedures are successfully handled by agents vs. those that frequently fail or require human intervention.
- **Standardization Heatmap**: Visualization of how consistently the organization is following defined procedures.
