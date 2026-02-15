# Antigravity Multi-Agent UX

As the system evolves to support swarms of coordinated agents, the UI must visualize the collaboration between different specialized AI entities.

## 1. Swarm Visualization
- **Agent Avatars**: Each specialized agent (e.g., Planner, Researcher, Coder, Reviewer) has a distinct visual identity (color/icon).
- **Communication Flow**: A visual "Message Bus" showing information passing between agents.
- **Hierarchy View**: For complex tasks, show the "Lead Agent" and its "Sub-agents" in a tree structure.

## 2. Coordination Traces
The Decision Trace expands to show multi-agent interactions.
- **Agent Attribution**: Every entry in the Trace Panel is tagged with the agent that produced it.
- **Handoff Markers**: Clear visual indicators when one agent completes a sub-task and hands the context to another.
- **Internal Debates**: If agents disagree (e.g., Coder vs. Reviewer), the UI visualizes the "Conflict & Resolution" process.

## 3. Shared Context Panels
- **Central Workspace**: A unified view where all agents contribute to the same set of artifacts.
- **Resource Ownership**: Show which agent is currently "using" or "locking" a specific tool or data source.

## 4. Leaderboard & Specialization
- **Agent Performance**: A dashboard showing the success rates and efficiency of different specialized agents.
- **Skill Discovery**: A list of specialized agents currently available in the swarm and their specific capabilities.

## 5. Control & Oversight
- **Global Kill-switch**: A single button to stop all agents in a swarm simultaneously.
- **Role Assignment**: Allow the operator to manually assign specific agents to specific steps in the plan.
