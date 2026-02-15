# Antigravity Tool Registry UX

The Tool Registry is where the agent's capabilities are managed and discovered. This document defines the UX patterns for tool orchestration and visibility.

## 1. Tool Discovery & Directory
- **Registry View**: A searchable grid of all available tools.
- **Tool Categories**: Filter by function (e.g., "Knowledge Extraction," "Automation," "Communication," "Data Analysis").
- **Capability Cards**: Each tool displays its "Primary Capability" (e.g., "Searches web for current events") and a list of required inputs.

## 2. Connection & Authorization
- **Status Badges**: `Connected`, `Authorization Required`, `Error`, or `Disabled`.
- **OAuth Integration**: Standardized button-led flow for connecting external SaaS tools (Slack, Notion, etc.).
- **Manual Config**: For database or custom API tools, provide a structured form for entering connection strings and secrets (securely masked).

## 3. Tool Performance Monitoring
- **Success Rate**: A metric showing how often the tool successfully completes its requested action.
- **Average Latency**: Insight into how "fast" the tool is, helping users optimize their workflows.
- **Usage History**: A list of tasks where the tool was recently used.

## 4. Custom Tool SDK Surface
For developers adding their own capabilities:
- **Test Bench**: A sandbox UI where developers can manually trigger a tool with sample inputs and see the raw JSON output.
- **Schema Validator**: Real-time feedback on the tool's input/output JSON schema.

## 5. Agent-Tool Interaction UX
- **Tool Selection Visualization**: During the planning phase, show which tools the agent has "selected" for each step.
- **Missing Tool Warning**: If a user goal requires a capability that isn't in the registry, the agent should proactively suggest which integration to connect.
