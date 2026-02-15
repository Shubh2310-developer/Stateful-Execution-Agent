# Antigravity Admin Settings Patterns

Admin Settings provide system-wide configuration and governance controls. This document defines the UX patterns for administrative oversight.

## 1. High-Level Categories
- **General**: Site name, timezone, global defaults.
- **Users & Teams**: RBAC, invite flow, activity monitoring.
- **Security & Compliance**: API keys, MFA enforcement, data retention policies, audit log access.
- **Integrations**: System-wide tool registry management.
- **LLM Settings**: Provider selection, global temperature, rate limit management.

## 2. Governance Controls
- **Safety Guardrails**: A UI to define "Forbidden Goals" or "Restricted Tools" for the entire organization.
- **Review Policy**: Configure which actions *always* require human-in-the-loop approval.
- **Data Retention**: Set global rules for how long State Snapshots and Artifacts are preserved before auto-deletion.

## 3. User & Team Management
- **Role Matrix**: A visual table where admins can toggle permissions for different user roles (Operator, Viewer, Auditor).
- **Seat Management**: Add/Remove users and see their last login and activity level.
- **Team Isolation**: Configure whether teams can see each other's tasks and memory.

## 4. System-wide Audit Search
A specialized version of [Audit Log UX](./AUDIT_LOG_UX.md) with the ability to search across all users and teams.

## 5. Configuration Interaction Patterns
- **"Save" vs. "Apply"**: Differentiate between saving a setting and applying it immediately to running agents.
- **Settings Versioning**: Allow admins to "Rollback" the system configuration to a previous state if a change causes issues.
- **Impact Analysis**: Before a major change (e.g., switching the default LLM model), the UI shows a "Predicted Impact" report.
