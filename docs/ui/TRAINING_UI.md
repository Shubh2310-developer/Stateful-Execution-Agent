# Antigravity RLHF & Training UI Patterns

Reinforcement Learning from Human Feedback (RLHF) is how users fine-tune the agent's behavior. This document defines the patterns for "Teaching" the agent.

## 1. The "Compare & Rank" UI
- **Scenario**: The agent generates two alternative plans or artifacts.
- **Interface**: Side-by-side cards with a "Winner" button and a "Why?" text field.
- **Interaction**: Drag-and-drop ranking for when more than two options are presented.

## 2. Inline Logical Corrections
- **"Teach Mode"**: A toggle in the Decision Trace that allows users to edit the agent's internal logic steps.
- **Pattern Learning**: "When I correct you like this, apply it to all future tasks of type X."
- **Visual Feedback**: The UI shows a "Success" pulse in the Memory tab when a correction is successfully generalized.

## 3. Dataset Curation
- **Exemplar Library**: A UI where users can mark specific tasks as "Perfect Examples" for the agent to use in future few-shot prompting.
- **Negative Examples**: Mark "Failures" to ensure the agent learns what *not* to do.

## 4. Fine-tuning Dashboard
- **Model Evolution Graph**: A chart showing the improvement in agent accuracy over time based on human feedback.
- **Feedback Heatmap**: Visualizing which types of tasks receive the most (or least) corrections.
- **Active Learning Queue**: The agent proactively asks the user to review "Ambiguous" historical decisions to improve its certainty.

## 5. Training Governance
- **Reviewer Workflow**: In large teams, "Expert Feedback" can be reviewed by an Admin before being committed to the global agent instructions.
- **Undo Training**: A way to "Rollback" the agent's learning if a batch of feedback was incorrect or biased.
