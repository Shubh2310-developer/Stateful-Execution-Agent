# Antigravity Token Budgeting UX

Managing spend in an agentic system is critical for enterprise adoption. This document defines the patterns for granular token and cost management.

## 1. The "Safety Valve" Budget
- **Task-level Limit**: When initiating a task, users can set a "Max Spend" (e.g., $5.00).
- **Hard vs. Soft Caps**:
  - *Soft Cap*: Notify the user when the limit is hit.
  - *Hard Cap*: Stop agent execution immediately when the limit is hit.
- **Remaining Runway**: A real-time countdown showing "Approx. reasoning steps remaining" based on current spend.

## 2. Budgetary Checkpoints
- **High-Cost Warnings**: If the agent calculates that a plan will likely exceed the typical task cost, it triggers a [Human-in-the-loop Checkpoint](./HITL_UX_PATTERNS.md).
- **Efficiency Suggestions**: "I can complete this task for 40% less using Haiku instead of Opus. Would you like to switch?"

## 3. Organizational Quotas
- **Team Wallets**: Admins can allocate specific "Token Credits" to different teams or projects.
- **Usage Bars**: Progress bars showing team-level consumption against monthly quotas.
- **Overdue Alerts**: High-visibility banners for accounts with exhausted budgets.

## 4. Cost Attribution UX
- **Project Tagging**: A field in the task creation form to assign costs to a specific billing code.
- **Step-by-step Billing**: In the Decision Trace, show the exact cost of each atomic decision or tool call.

## 5. Financial Analytics
- **Projected Spend**: A predictive chart showing estimated end-of-month costs based on current task volume.
- **ROI vs. Cost**: (See [ANALYTICS_UX.md](./ANALYTICS_UX.md)) - Correlating spend with "Time Saved" to prove the value of the agent.
