# Antigravity Permission Matrix UX

Managing complex Role-Based Access Control (RBAC) in a multi-user agentic system requires a high-density, intuitive matrix interface.

## 1. Matrix Layout
- **Vertical Axis**: Resources (Tools, Memory, Organizations, Task Types).
- **Horizontal Axis**: Roles (Admin, Operator, Reviewer, Viewer, Custom).
- **Interaction**: A grid of toggles or checkboxes.

## 2. Capability Levels
Permissions aren't just "On/Off." We use tiered access levels:
- **No Access**: (Empty)
- **View Only**: Can see traces and artifacts but cannot initiate or approve.
- **Full Control**: Can initiate tasks and manage the tool registry.
- **Restricted**: Can only execute specific, pre-approved [Task Templates](./TASK_TEMPLATE_UX.md).

## 3. Scoped Permissions (Team/User level)
- **Inheritance Visualization**: Use muted icons to show permissions inherited from an organization level, which can be overridden at the team or user level.
- **Exclusion Rules**: A dedicated section for "Explicit Denials" (e.g., "User X can do everything *except* access the Financial tool").

## 4. Temporary & Just-in-Time Access
- **Time-bound Permissions**: A "Duration" selector next to a permission toggle (e.g., "Grant access for 24 hours").
- **Request Flow**: A "Request Access" button that appears when a user encounters a restricted resource, triggering a notification to an Admin.

## 5. Security Audit Integration
- **Permission History**: A "Change Log" specifically for the permission matrix, showing who changed which rule and when.
- **Risk Assessment**: A small gauge that calculates a "Security Risk Score" based on the current matrix configuration (e.g., "Warning: Too many users have 'Delete' permissions").
