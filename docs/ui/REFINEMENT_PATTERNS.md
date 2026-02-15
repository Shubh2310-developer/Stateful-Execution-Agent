# Antigravity Refinement Patterns

The "Refinement Loop" is the most critical interaction point between the operator and the agent. This document defines the UI patterns for iterative artifact improvement.

## 1. The Refinement Input

After an artifact (e.g., a document or report) is generated, a persistent input area appears at the bottom of the Workplace.

- **"Always-on" Feedback**: The input should be prominent but not intrusive, labeled "How can I improve this?" or "Request adjustments."
- **Contextual Suggestions**: Above the input, show 2-3 "Smart Suggestions" based on common refinements for the current artifact type.
  - *Example (for a report)*: "Make it more concise," "Add more data visualizations," "Change tone to technical."

## 2. Inline Selection & Commenting

Users should be able to refine specific parts of an artifact without regenerating the whole thing.

- **Highlight to Refine**: If the user highlights a paragraph in a Markdown document, a small floating menu appears with an "Edit" option.
- **Precision Corrections**: "In this section, replace the revenue figure with the updated number from the Slack channel."
- **Visual Feedback**: Use a "Ghost Text" or "Strikethrough" effect to show what the agent is planning to change before committing the update.

## 3. Version Comparison (Diff View)

Refinement creates multiple versions of an artifact. Users need to compare them.

- **Split-screen Diff**: A classic side-by-side view showing "Before" and "After" changes.
- **Change Summary**: The agent provides a 1-sentence summary of the refinements made (e.g., "Refined the summary to be 20% shorter and added the feasibility section as requested").
- **Restore Version**: A single-click button to revert to a previous version if a refinement was unsuccessful.

## 4. Multi-modal Refinement

Refinement isn't just for text.

- **Chart Tweaking**: "Change this bar chart to a line graph" or "Use a different color scheme."
- **Plan Adjustment**: "Add an extra step after the analysis to verify the findings with the engineering lead."
- **Memory Correction**: "Actually, I prefer my reports in PDF format from now on." (The UI should highlight that this has now been saved to long-term memory).

## 5. Transitioning from Refinement to Completion

- **"Finalize" Action**: Once the user is satisfied, a clear "Finalize" button commits the artifact and triggers the final task-completion memory update.
- **Feedback Collection**: A final star-rating and text box appear, closing the loop and confirming the agent's learning.
