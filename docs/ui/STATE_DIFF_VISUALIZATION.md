# Antigravity State Diff Visualization

State Diffs allow operators to understand exactly how a task's state has evolved between versions. This is critical for auditing, debugging, and understanding the agent's iterative progress.

## 1. The "State Delta" Principle
Instead of showing two full state objects, we prioritize showing the **Change**.
- **Added**: Highlighted in Emerald (`text-emerald-600`, `bg-emerald-50`).
- **Removed**: Highlighted in Red (`text-red-600`, `bg-red-50`).
- **Modified**: Highlighted in Blue (`text-blue-600`, `bg-blue-50`).

## 2. Visual Diff Modes

### A. Semantic Diff (The Human View)
A high-level summary of the changes in plain language.
- *Example*: "Added 3 new risks to the risk register; updated Step 3 status to 'Completed'; learned that user prefers bullet points."

### B. Technical Diff (The JSON View)
A structured, code-like view showing the exact changes in the state JSON.
- **Unified Diff**: Changes shown inline.
- **Split Diff**: Side-by-side comparison of Version X and Version Y.
- **Path Highlighting**: A sidebar showing the JSON keys that were modified (e.g., `plan.steps[2].status`).

### C. Visual State Graph Diff
Highlighting changes directly on the [State Visualization Graph](./STATE_VISUALIZATION.md).
- Modified nodes pulse gently.
- New edges are drawn with a distinct color.

## 3. Filtering the Diff
Since state objects can be large, allow users to filter the diff by category:
- `[ ] Plan Changes`
- `[ ] Artifact Updates`
- `[ ] Memory Learning`
- `[ ] Decision Trace Additions`

## 4. Navigation & Context
- **Version Selector**: A timeline or dropdown to select the "Baseline" and "Comparison" versions.
- **Jump to Trace**: Click any diff entry to see the Decision Trace entry that *caused* that specific state change.

## 5. Interaction Patterns
- **Hover for Detail**: Hover over a modified field to see its previous value in a tooltip.
- **Expand/Collapse**: Group changes by their top-level JSON key and allow the user to collapse sections that aren't relevant to their audit.
