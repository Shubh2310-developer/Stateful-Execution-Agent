# Antigravity Prompt Editor UX

As a stateful agent, Antigravity's behavior is driven by its instructions. The Prompt Editor UI allows advanced users to "tune" the agent's core logic safely.

## 1. Visual Environment
- **Code-focused**: Use the [Dark Mode](./DARK_MODE.md) code background (`#111827`) with syntax highlighting for Jinja2 or Markdown.
- **Variable Highlighting**: Clearly distinguish between static instructions and dynamic variables (e.g., `{{ user_goal }}`).
- **Version Sidebar**: A list of previous prompt versions with the ability to "Compare" or "Rollback."

## 2. Safe Editing Patterns
- **Draft Mode**: All changes are saved as "Drafts" first. They must be "Tested" before being deployed to the live agent.
- **Instruction Guardrails**: Real-time feedback if a user removes a critical system constraint (e.g., "Warning: You removed the safety validation block").
- **Template Gallery**: Access to "Tested Instruction Sets" for different domains (e.g., "Legal Compliance Analyst," "Creative Writing Assistant").

## 3. Testing & Simulation
- **Sandbox Execution**: A split-screen view where users can enter a sample goal and see how the *modified* prompt changes the generated plan.
- **Diff Comparison**: Side-by-side view of the "Current Agent Output" vs. the "Modified Agent Output."
- **Token Estimation**: Real-time calculation of how the prompt length affects the cost of each task.

## 4. Collaborative Prompting
- **Peer Review**: Allow users to request a review of a prompt change from another team member before it is finalized.
- **Commentary Blocks**: Allow users to leave "Reasoning" notes inside the prompt editor that aren't sent to the LLM but explain the logic to other operators.

## 5. Security & Governance
- **Scoped Editing**: Only users with the `Prompt Engineer` or `Admin` role can access the editor.
- **Global Constraints**: A "Read-only" section of the system prompt that enforces organizational safety and privacy rules, which cannot be modified by standard operators.
