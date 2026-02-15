# Antigravity Memory Management UX

The agent's long-term memory is its greatest asset. The Memory Curation UI allows users to audit, edit, and optimize what the agent has learned.

## 1. Memory Audit Interface
A searchable list of all "Learned Facts" and "Patterns."

- **Fact Cards**: Each memory entry is represented as a card.
  - **Source**: Where the fact was learned (Task ID, Integration, or Manual Entry).
  - **Confidence**: How "sure" the agent is about this fact.
  - **Last Used**: When this memory last influenced a decision.
- **Filtering**: Filter by category (e.g., "Preferences," "Domain Knowledge," "Formatting").

## 2. Curation Controls (Editing & Deletion)
Users must have ultimate control over the agent's knowledge.

- **Edit Mode**: Allow users to manually correct a learned preference (e.g., "Actually, I want my reports in Markdown, not PDF").
- **Purge Action**: A "Forget" button to immediately delete a memory entry.
- **Conflict Resolution**: If the agent has learned two contradictory facts, the UI should flag this and ask the user to select the "True" one.

## 3. Active Learning (Teaching)
A proactive way to improve the agent without waiting for it to learn from experience.

- **Manual Preference Entry**: A form where users can state explicit rules: "Always use the metric-heavy template for investor updates."
- **Context Injection**: Allow users to upload "Reference Documents" that the agent should use as the "Source of Truth" for certain domains.

## 4. Visualization of Influence
- **Decision Mapping**: When viewing a memory entry, show a "History of Influence" — a list of tasks where this specific memory entry changed the outcome.
- **Association Graph**: A visual map showing how different memory entries relate to each other (e.g., "Metric Preferences" linked to "Financial Domain Knowledge").

## 5. Privacy & Export
- **Memory Portability**: A way to export learned patterns as a JSON file to "transfer" the agent's knowledge to a different environment.
- **Privacy Toggles**: Mark specific memory entries as "Private" (available only to the user) or "Global" (shared across the team).
