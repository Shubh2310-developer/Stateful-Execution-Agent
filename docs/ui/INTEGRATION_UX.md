# Antigravity Integration UX

As a stateful execution agent, Antigravity interacts with a wide array of third-party tools and platforms. This document defines how these integrations are presented to the user to ensure a seamless "Unified Workspace" experience.

## 1. Tool Registry Interface

The Tool Registry is where users manage what the agent can access.

- **Integration Cards**: Each tool (e.g., Slack, MongoDB, Google Drive) is represented by a card featuring its official icon, status (Connected/Disconnected), and a list of authorized capabilities (e.g., "Read Messages," "Post Updates").
- **Connection Flow**: Use a standardized OAuth or API Key entry modal for all integrations. Provide clear instructions on where to find the required credentials.
- **Health Indicators**: Real-time status icons. A red dot indicates an integration is failing (e.g., expired token), while green indicates it's ready for use.

## 2. Tool Usage in the Decision Trace

When the agent invokes an external tool, the UI must make it clear.

- **Tool Badges**: Use small, recognizable badges in the Trace Panel when a tool is called.
  - *Example*: `[Slack] Post update to #product-updates`.
- **Input/Output Previews**: Allow users to expand a tool call entry to see exactly what data was sent to the integration and what was returned.
- **Latency Visualization**: Show a small timer next to tool calls that are taking longer than average, keeping the user informed of external delays.

## 3. Inline Integration Surfaces

Sometimes the agent's work happens *within* another tool's context.

- **Slack/Teams Notifications**: When an agent completes a task or requires approval, it can post a message. These messages should be formatted using the platform's rich UI (e.g., Slack Block Kit) to provide "App-like" buttons for "Approve" or "Review" directly in the chat.
- **Browser Overlay**: For web-search or data-extraction tasks, a subtle browser overlay can show what the agent is currently "looking at," providing visual confirmation of the agent's focus.

## 4. Federated Memory

Integrations can also contribute to the agent's long-term memory.

- **Source Attribution**: In the Memory view, show which integration provided a specific piece of knowledge.
  - *Example*: "Preferred report format learned from 12 Slack messages in #reports."
- **Synching Controls**: Allow users to toggle which integrations are allowed to "teach" the agent.

## 5. Artifact Destination UX

- **Export Targets**: When an artifact is generated, provide "Send to..." options for all connected platforms (e.g., "Save to Google Drive," "Attach to Jira Issue").
- **Auto-Syncing**: Allow users to configure "Auto-export" rules (e.g., "Always save investor updates to the 'Investor Relations' folder in Dropbox").
