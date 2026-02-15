# Antigravity Instruction Versioning UX

As a stateful agent, the core logic of Antigravity is driven by system instructions (prompts). This document defines the UI patterns for managing, comparing, and rolling back versions of these instructions.

## 1. The Instruction Timeline
- **Version Nodes**: A vertical timeline showing the history of instruction updates.
- **Metadata**: Each version displays the author, the date of change, and a "Change Note" (e.g., "Optimized risk analysis weighting").
- **Deployment Status**: Clearly mark which version is currently "Live," "In Staging," or "Draft."

## 2. Comparison Mode (Diff View)
- **Side-by-Side Editor**: A specialized view showing the current live prompt vs. the proposed update.
- **Highlighting**: Use standard green/red diff highlighting for additions and deletions.
- **Variable Tracking**: If a new variable is introduced (e.g., `{{ user_timezone }}`), the UI flags it and asks for a "Default Mock Value" for playground testing.

## 3. Impact Analysis
- **Reasoning Shift**: A "Before and After" preview showing how the agent's reasoning on a standard set of tasks would change under the new instructions.
- **Token Variance**: Visual indicator showing if the new instructions are significantly longer (more expensive) or shorter.

## 4. Rollback Patterns
- **Safety Gate**: Rolling back to a previous instruction version requires a "Safety Confirmation" modal.
- **Reasoning Continuity**: When instructions are changed, the UI should flag any *active* tasks that were started under the previous version, offering to "Migrate" them or "Finish under old instructions."

## 5. Branching & Experiments
- **A/B Test View**: A dashboard for comparing two different instruction versions running on a split of incoming tasks.
- **Success Metrics per Version**: Compare the 1-5 star ratings and success rates of tasks executed under Version A vs. Version B.
