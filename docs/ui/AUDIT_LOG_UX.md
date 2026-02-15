# Antigravity Audit Log UX

For enterprise compliance and security, Antigravity maintains an immutable, cryptographically signed log of every action taken by the system and its users.

## 1. High-Density Audit View
- **Tabular Layout**: A professional, column-heavy table optimized for scanning.
- **Core Columns**:
  - `Timestamp` (UTC)
  - `User/Agent ID`
  - `Action Type` (e.g., Task Created, Secret Accessed, State Rollback)
  - `Resource` (The specific task, tool, or memory entry affected)
  - `Status` (Success/Failed)
  - `IP/Device`

## 2. Deep Search & Filtering
- **Event Categorization**: Filter by "Security Events," "Financial Events (Cost)," "Task Execution," or "Memory Changes."
- **Time Range Deep-dive**: High-resolution time selectors (down to the millisecond).
- **Full-text Search**: Search within the raw payloads of the audit entries.

## 3. Evidence Collection
- **Audit Export**: Generate a "Certificate of Execution" — a signed PDF summarizing the entire task lifecycle, decision trace, and artifacts for legal review.
- **State Proofs**: Link audit entries directly to the versioned [State Snapshots](./VERSIONING_UX.md).
- **Snapshot Export**: Download the raw JSON of a specific state version as "Digital Evidence."

## 4. Security Alerts
- **Anomalous Activity**: Highlight entries that represent security risks (e.g., "10 consecutive failed auth attempts").
- **Integrity Checks**: A "Validate Log" button that checks the cryptographic hashes of the audit trail to ensure no entries have been tampered with.

## 5. Accessibility for Compliance Officers
- **Plain Language Summaries**: Next to the technical log entry, provide a human-readable summary (e.g., "The agent sent an email to client@example.com using the Gmail tool").
- **Read-only Mode**: Ensure the Audit UI is strictly read-only for compliance roles, preventing any accidental modification of logs.
