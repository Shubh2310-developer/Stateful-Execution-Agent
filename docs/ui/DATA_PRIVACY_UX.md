# Antigravity Data Privacy UX Guidelines

Data privacy is a foundational pillar of the Antigravity trust model. This document defines the UI patterns that empower users to control, monitor, and protect their data.

## 1. The Privacy Control Center
A centralized hub in the user settings for managing data footprints.

- **Data Retention Toggles**: Granular controls for how long task logs, artifacts, and traces are stored (e.g., 24h, 30 days, Forever).
- **"Forget Me" Action**: A single-click button to purge all personal data, including learned preferences and long-term memory.
- **Privacy Audit Log**: A view showing every instance where sensitive data was accessed or processed by an agent.

## 2. Real-time Privacy Shield
Visual indicators that active protection is working. (See [PRIVACY_SHIELD_UX.md](./PRIVACY_SHIELD_UX.md))

- **Auto-Redaction Badge**: A small shield icon in the header that pulses when PII is being filtered from the Decision Trace.
- **Redaction Context**: Users can hover over blurred text to see *why* it was redacted (e.g., "Redacted: Credit Card Number").

## 3. Contextual Data Scoping
Ensuring the agent only sees what it needs.

- **"Need-to-Know" Visualization**: When starting a task, show a list of the data sources the agent will access. Users can "Uncheck" specific folders or files to restrict access.
- **Task Isolation**: A visual indicator (e.g., a "Safe" icon) confirming that the current task's short-term memory is logically isolated and won't leak into other sessions.

## 4. Transparent Memory Curation
Transparency into the agent's learning process. (See [MEMORY_CURATION_UX.md](./MEMORY_CURATION_UX.md))

- **"Learned Fact" Approval**: Optionally require users to approve a fact before it is committed to long-term memory.
- **Fact Provenance**: Every piece of knowledge in the memory graph must link back to the specific task and user that generated it.

## 5. Privacy-First Copywriting
- **Ambiguity Reduction**: Instead of "We care about your privacy," use "Your data is encrypted end-to-end and never used for cross-organizational training."
- **Clear Consent**: Use "I Allow Agent to Learn" vs. "Execute without Learning" rather than hidden toggles.

## 6. Compliance Badging
- **Regional Toggles**: Clearly show if the UI is currently optimized for GDPR, CCPA, or other regional standards.
- **Export for Portability**: A "Download My Data" button that generates a standardized JSON package of all task history and memory.
