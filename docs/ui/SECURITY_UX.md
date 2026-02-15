# Antigravity Security & Privacy UX

In an agentic system with access to private data and external tools, security is a user experience priority. This document defines how the Antigravity UI communicates safety, privacy, and permissions.

## 1. Permission Visibility

Users must always know what the agent can and cannot do.

- **Tool Capabilities**: In the "New Task" and "Mission Control" views, clearly display the tools the agent is authorized to use for the current task.
- **Connection Status**: Use a "Secure Connection" badge to indicate encrypted communication with the LLM provider (Groq) and databases.
- **Data Boundary Visualization**: Clearly mark if the agent is accessing internal (private) vs. external (public) data sources using distinct visual borders or background tints.

## 2. High-Impact Approval (The "Gatekeeper" Pattern)

For operations that are destructive or external-facing, the UI enforces a manual approval step.

- **Action Interstitials**: When the agent wants to perform a high-impact action (e.g., `delete_file`, `send_email`), the UI presents a "Security Authorization" card.
- **Visual Distinction**: Use the **CTA Color** (#F97316) or **Warning Color** (#F59E0B) for these cards to differentiate them from standard reasoning entries.
- **Explicit Consent**: Use clear, non-ambiguous labels: "Authorize Action" vs. "Deny Action."

## 3. Privacy Preservation

- **Sensitive Data Masking**: In the Decision Trace, automatically mask common PII (Personal Identifiable Information) patterns (emails, keys, credit card numbers) unless the user explicitly toggles "Show Sensitive Data."
- **Context Isolation**: When viewing a task, show a visual indicator that the agent's current "Short-term Memory" is isolated to this specific task and will not leak into other users' sessions.
- **"Forget This" Actions**: Allow users to click a "Delete from Memory" icon next to any learned preference or fact to immediately purge it from the long-term memory store.

## 4. Audit & Compliance UX

- **Immutable Logs**: Ensure the user understands that the Decision Trace is append-only and cannot be altered, serving as a legal/security audit log.
- **Export for Audit**: Provide a "Download Audit Log" button that exports the entire task state and trace as a signed PDF or JSON file.
- **User Attribution**: In multi-user environments, clearly display who initiated the task and who approved specific checkpoints.

## 5. Security Copywriting

- **Transparent Explanations**: Instead of "Permission Denied," use "This task requires the `web_search` tool, which is currently disabled in your security settings."
- **Clarity over Technicality**: Explain the *impact* of a security decision, not just the technical rule.
