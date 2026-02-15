# Antigravity Human-in-the-loop Deep Dive Patterns

For complex or high-risk tasks, a simple "Approve/Deny" is not enough. This document defines deep collaboration patterns for Human-in-the-loop (HITL) workflows.

## 1. Collaborative Planning (Interactive Roadmap)
- **Step Negotiation**: Users can drag to reorder steps, click to edit success criteria, or insert "Human Checkpoints" manually into the plan.
- **Alternative Path Review**: The agent presents 3 different strategies for a goal and asks the user to "Vote" on the best path.

## 2. Inline Reasoning Correction
- **Thought Editing**: In the Decision Trace, users can click a "Reasoning Block" and correct the agent's logic: "Your assumption that we need a PDF is wrong; we only need a CSV."
- **Knowledge Injection**: "Here is a piece of information you missed: [Paste text/Upload file]." The agent immediately incorporates this into the active step's context.

## 3. "Ride-along" Debugging
- **Manual Overdrive**: An advanced mode where the operator can manually "Take Control" of a specific tool call, enter the parameters themselves, and then hand control back to the agent.
- **Breakpoints**: Allow users to set "Stop Conditions" (e.g., "Pause if the cost exceeds $5").

## 4. Multi-party Consensus
- **The Review Committee**: For organizational sign-off, a task can require multiple users to "Sign-off" on an artifact.
- **Consensus Dashboard**: Shows who has approved, who has requested revisions, and the "Final Decision" logic.

## 5. Feedback Loop Analytics
- **"Teaching" Dashboard**: Analytics showing how much the agent's accuracy has improved *because* of specific human interventions.
- **Correction Categories**: Track common types of human corrections (e.g., "Tone Adjustment," "Data Source Correction") to identify areas where the agent's system prompt needs tuning.
