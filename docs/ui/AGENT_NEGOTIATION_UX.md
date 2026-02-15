# Antigravity Agent Negotiation UX

Negotiation occurs when an agent proposes a plan that conflicts with user preferences, or when two specialized agents disagree on a path.

## 1. User-Agent Negotiation
- **The "Counter-proposal" UI**: When a user rejects a plan, the agent presents an alternative with a "Comparison Table" showing pros/cons of both approaches.
- **Constraint Bargaining**: "I can meet your deadline if we skip the detailed risk analysis. Should I proceed?"
- **Tone Adjustment**: If a user finds a plan "Too aggressive," the agent offers a "Softer" version with more checkpoints.

## 2. Agent-to-Agent Disagreement
- **The "Internal Debate" Panel**: A split-view within the Decision Trace showing two specialized agents (e.g., Coder vs. Tester) arguing their logic.
- **Evidence Weighting**: Visualizing the data points each agent is using to justify its position.

## 3. Human Arbitration UI
- **The "Judge" Role**: A specialized interface for the operator to resolve an inter-agent conflict.
- **Conflict Summary**: "Agent A prioritizes speed; Agent B prioritizes precision. Who is correct for this mission?"
- **Logic Selection**: Allow the user to select specific logical points from both sides to form a hybrid "Consensus" path.

## 4. Compromise Visualization
- **The "Third Way"**: The agent suggests a compromise path that incorporates feedback from both sides of the conflict.
- **Alignment Gauge**: Showing how the current compromise aligns with the user's overall [Design Principles](./DESIGN_PRINCIPLES.md).

## 5. Learning from Negotiation
- **Policy Record**: A negotiation result is saved as a "Golden Rule" in the [Memory Curation](./MEMORY_CURATION_UX.md) view.
- **Friction Reduction**: Tracking "Successful Resolutions" to automatically resolve similar conflicts in the future.
