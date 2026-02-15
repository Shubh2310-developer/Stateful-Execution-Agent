# Antigravity Human-in-the-loop (HITL) Patterns

Deep collaboration between human operators and autonomous agents is a core Antigravity feature. This document defines the patterns for "Mission Partner" interactions.

## 1. The Checkpoint Card
- **Trigger**: The agent hits an ambiguity or high-risk step.
- **Content**:
  - **The Ask**: A clear question (e.g., "Which data source should I prioritize?").
  - **The Options**: 2-3 agent-suggested paths with pros/cons.
  - **The Context**: Links to the specific trace entries or memory facts that led to this checkpoint.

## 2. Collaborative Planning
- **The "Draft Plan" View**: Before execution, the agent presents a proposal.
- **Interactive Editing**: Users can delete steps, reorder them, or add "Human-Only" sub-tasks (e.g., "Wait for me to call the client").
- **Negotiation Trace**: A log of how the plan changed based on user-agent discussion.

## 3. Real-time Intervention (Barge-in)
- **The "Steer" Control**: A prominent button in Mission Control that pauses execution and opens a dialogue: "Wait, do [this] instead."
- **Knowledge Injection**: A "Note to Agent" field where users can add ephemeral context that only applies to the current task.

## 4. Joint Artifact Authorship
- **Split Editing**: A view where the agent and user can edit the same document.
- **Agent Suggestions**: The agent highlights text and suggests "I could expand this section based on the Q3 data. Should I?"
- **Accept/Reject Flow**: A list of agent-proposed changes that the user can batch-approve.

## 5. Trust & Feedback Analytics
- **Collaboration Ratio**: A metric showing the balance of "Autonomous Steps" vs. "Human Interventions."
- **Teaching Score**: How many times a human intervention led to a new learned preference in the [Memory Curation](./MEMORY_CURATION_UX.md) view.
- **Partner Calibration**: A setting to adjust how "Needy" the agent is (from "Maximum Autonomy" to "Step-by-Step Approval").
