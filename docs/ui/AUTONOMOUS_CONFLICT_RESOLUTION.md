# Antigravity Autonomous Conflict Resolution UX

In multi-agent swarms, agents may occasionally disagree on logic, tools, or outputs. This document defines how these conflicts are visualized and resolved.

## 1. Conflict Visualization (The "Debate" Pattern)
- **Side-by-Side Reasoning**: When two agents disagree, the Decision Trace shows their conflicting logic in two parallel columns.
- **Agent Attribution**: Clearly mark which agent is holding which position (e.g., "Researcher proposes Source A; Reviewer proposes Source B").
- **Evidence Stacking**: List the supporting data points for each side of the conflict.

## 2. Autonomous Resolution Trace
- **The Arbiter Agent**: A specialized "Lead" agent analyzes the disagreement and makes a final decision.
- **Resolution Rationale**: A trace entry explaining *why* one path was chosen over the other.
  - *Example*: "Arbiter selected Researcher's path because Source A is a primary dataset whereas Source B is an unverified aggregate."

## 3. Human Intervention in Conflicts
- **"Tie-breaker" CTA**: If the agents cannot resolve the conflict autonomously, the UI presents a [Checkpoint Card](./HITL_UX_PATTERNS.md) for the user to decide.
- **Consensus Voting**: In high-stakes organizations, allow multiple team members to vote on the resolution path.

## 4. Conflict Analytics
- **Disagreement Rate**: A metric showing how often agents in a swarm disagree, helping to identify "Noisy" or poorly tuned agents.
- **Correction Heatmap**: Identifying which tools or domains cause the most internal swarm friction.

## 5. Learning from Conflict
- **Consensus Refinement**: If a human tie-breaker is used, the agent saves the decision as a "Policy" for future similar conflicts.
- **Trace Replay**: Allow developers to replay a conflict in the [Prompt Playground](./PROMPT_PLAYGROUND_UX.md) to adjust the agents' underlying instructions.
