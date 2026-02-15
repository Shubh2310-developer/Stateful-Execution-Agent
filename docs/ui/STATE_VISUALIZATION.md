# Antigravity State Visualization Strategy

Visualizing the internal state of a complex, autonomous agent is critical for trust and debuggability. This document outlines how Antigravity represents task trees, memory clusters, and execution flows.

## 1. Task Tree & Plan Visualization

Plans are rarely linear. They often have dependencies, parallel branches, and conditional loops.

- **Dynamic DAG (Directed Acyclic Graph)**: Represent the execution plan as a graph.
  - **Nodes**: Plan steps.
  - **Edges**: Dependencies.
  - **State Coloring**: Gray (Pending), Blue Pulse (Running), Emerald (Success), Red (Failed).
- **Zoomable Canvas**: Use an infinite canvas approach (e.g., React Flow) to allow users to zoom into specific sub-tasks or zoom out to see the entire mission goal.
- **Breadcrumbs of Autonomy**: A horizontal timeline showing the "History of Intent" — how the plan has evolved in response to environment feedback.

## 2. Memory Cluster Visualization

Long-term memory is a high-dimensional vector space. We simplify this for the user.

- **Knowledge Cards**: Group learned facts into semantic clusters (e.g., "User Preferences," "Domain Terms," "Historical Patterns").
- **Association Mapping**: Show links between a specific decision in the Trace and the memory entry that influenced it.
- **Confidence Heatmaps**: Use color intensity to show how "certain" the agent is about a particular learned fact.

## 3. Decision Trace Flow

The "Heartbeat" of the agent.

- **Stream View**: A vertical feed of atomic decisions.
- **Filter & Search**: Allow operators to filter the trace by tool type, confidence score, or event category (e.g., "Show only tool errors").
- **Branching History**: When the agent retries a step or revises a plan, show the "failed branch" as a collapsed, muted section to preserve history without cluttering the current path.

## 4. Resource & Tool Utilization

- **Gantt-style Timeline**: Show when specific tools (APIs, Database, Web Search) were active.
- **Cost/Token Gauges**: Real-time visualizers for resource consumption, helping users understand the "cost of autonomy."

## 5. Success Criteria Dashboard

- **Checklist Radar**: A radar chart or multi-progress bar showing how close the agent is to fulfilling each requirement of the high-level goal.
- **Artifact Lineage**: A visual map showing how raw data from Step 1 was transformed into the final artifact in Step 5.
