# Antigravity Human Augmentation UX

Beyond task execution, Antigravity suggests ways for the *human operator* to be more efficient. This document defines the augmentation patterns.

## 1. The "Performance Co-pilot"
- **Interaction Analytics**: The agent monitors the user's interaction speed and error rate, suggesting [Keyboard Shortcuts](./SHORTCUT_REFERENCE.md) or [Command Palette](./COMMAND_PALETTE.md) patterns to speed up oversight.
- **Contextual Tips**: "I've noticed you spend a lot of time reviewing 'Risk Reports.' Would you like me to auto-summarize the high-priority items for you?"

## 2. Decision Support Systems
- **The "Wisdom of the Swarm"**: When a user is making a decision, the agent surfaces "How 5 other experts handled this" (anonymized/ZKP-protected).
- **Impact Simulation**: A "Sandbox" where a user can toggle a decision and see the predicted outcome on a generated chart before committing.

## 3. Cognitive Load Relief
- **Information Filtering**: Automatically hiding non-critical trace entries when the user's BCI or mouse movement indicates high cognitive load.
- **Summary Mode**: A "Focus Mode" that collapses everything except the active artifact and a high-level success checklist.

## 4. Skill Transfer (Learning from the Agent)
- **"Why I did this" Tutorials**: In-depth logical explanations for complex agent choices that serve as mini-lessons for the operator in a new domain.
- **Terminology Onboarding**: Automatic [Glossary](./GLOSSARY.md) lookups for domain-specific terms the agent uses.

## 5. Proactive Handoffs (The "Your Turn" Signal)
- **Preparation Toasts**: "I'll be ready for your review in 2 minutes. Here is the background data you'll need."
- **Digest Previews**: A 1-sentence summary sent to the user's phone *before* they open the desktop, helping them "Spin up" their context mentally.
