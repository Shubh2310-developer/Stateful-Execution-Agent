# Antigravity Agent Profiling UX

Agent Profiling provides deep insight into the performance, personality, and effectiveness of individual specialized agents within the Antigravity swarm.

## 1. Agent Identity Cards
Every agent (Planner, Researcher, Coder, etc.) has a profile page containing:
- **Core Skillset**: A list of the agent's primary capabilities and authorized tools.
- **Personality Traits**: Visual gauges for traits like "Thoroughness," "Directness," and "Creativity" (derived from their system instructions).
- **Integration Status**: Which third-party tools the agent is currently configured to use.

## 2. Performance Analytics (Per Agent)
- **Success Rate**: Historical percentage of sub-tasks successfully completed without human intervention.
- **Efficiency Score**: Average time taken to complete tasks relative to the swarm average.
- **Confidence Calibration**: A chart showing the correlation between the agent's *predicted* confidence and its *actual* success rate.

## 3. Learning & Adaptation Trace
- **Learned Heuristics**: A list of patterns this specific agent has learned (e.g., "The Researcher has learned to prioritize PDF sources for financial data").
- **Constraint Compliance**: A log of how often the agent successfully follows specific user-imposed constraints.

## 4. Collaborative Influence
- **Relationship Map**: A visualization showing which agents this agent interacts with most frequently (e.g., "The Planner frequently hands off to the Researcher").
- **Reviewer Feedback**: If a Reviewer agent corrected this agent, show a log of the "Peer Review" sessions and what was adjusted.

## 5. Visual Representation
- **Unique Avatars**: Distinct icons and color themes for each agent type (see [PERSONA_DESIGN.md](./PERSONA_DESIGN.md)).
- **Status Indicators**: Real-time indicators of what the agent is doing (e.g., "The Researcher is currently idling," "The Coder is active on task_001").
- **Badge System**: Award badges for specific "Expertise" demonstrated by the agent (e.g., "Web Search Specialist," "Data Analysis Pro").
