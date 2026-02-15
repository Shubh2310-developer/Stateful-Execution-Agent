# Antigravity Slack App Integration UX

The Slack integration brings Antigravity's operational transparency into the primary communication hub of the enterprise.

## 1. Home Tab (The Dashboard)
- **Overview**: A view of all active missions within the user's Slack workspace.
- **Quick Actions**: "Launch Mission," "Open Registry," "Check Health."

## 2. Interactive Decision Traces
- **Block Kit Formatting**: Every entry in the Decision Trace is posted as a Slack message block.
- **Visual Cues**: Use Slack's standard color strips (Blue for Info, Amber for Checkpoint, Red for Error).
- **Reasoning Snippets**: Collapsible sections using Slack's `accessory` blocks for deep-dive logic.

## 3. Approvals & Checkpoints
- **Button Actions**: "Approve," "Deny," and "Refine" buttons directly within the message.
- **Modals**: Clicking "Refine" opens a Slack modal for entering structured feedback.

## 4. Slashing Commands
- `/antigravity status [task_id]`: Fetch current progress.
- `/antigravity pause [task_id]`: Stop execution.
- `/antigravity learn "[fact]"`: Manually inject knowledge into the agent's long-term memory.

## 5. Artifact Previews
- **Unfurling**: When an Antigravity artifact URL is pasted into Slack, the app "unfurls" it to show a rich preview (Summary, Metrics, Chart).
- **Direct Download**: Buttons to download the PDF or JSON artifact without leaving the thread.

## 6. Notification Channels
- **Mission Channels**: Automatically create or post to specific channels for team-based task monitoring.
- **DMs**: Private, high-priority alerts for personalized tasks.
