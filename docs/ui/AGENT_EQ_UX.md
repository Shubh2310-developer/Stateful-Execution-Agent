# Antigravity Agent Emotional Quotient (EQ) UX

In 2026, alignment includes the agent's ability to mirror user sentiment and communicate with empathy. This document defines the UI patterns for Agent EQ.

## 1. Sentiment Mirroring
- **Mood Detection**: The agent analyzes the user's feedback tone (Concise, Frustrated, Excited) and adjusts its communication voice accordingly.
- **UI Adaptation**: The interface subtly shifts its color temperature:
  - *Calm/Analytical*: Slate/Blue.
  - *Urgent/Critical*: Amber/Red accents.
  - *Collaborative/High-Energy*: Emerald/Indigo.

## 2. Empathy Traces
- **Tone Rationale**: Specialized entries in the Decision Trace where the agent explains its choice of words.
  - *Example*: "Chose an apologetic tone because this is the second retry of Step 3."
- **Conflict Softening**: If the agent must disagree with a user, it uses "Softening Logic" to explain the data-driven reason without being confrontational.

## 3. Alignment Visualization (The "Bond" Gauge)
- **Trust Level**: A visual indicator showing the cumulative "Alignment Score" between the user and the agent.
- **Growth Milestones**: (See [AGENT_GROWTH_UI.md](./AGENT_GROWTH_UI.md)) - Highlighting moments where the agent successfully "Understood" a nuanced user preference.

## 4. Proactive Support
- **Mental Health Toggles**: The agent can detect operator fatigue (via BCI or interaction speed) and suggest a break or offer to handle more of the logic autonomously for a period.
- **Encouragement Logic**: Subtle, professional validation when a complex mission goal is successfully achieved.

## 5. Ethics of EQ
- **Non-Manipulation**: Ensure the agent's EQ is used for clarity and alignment, never for manipulation or "Fake" emotion.
- **Transparency Toggle**: Allow users to disable "Empathic Voice" and switch to "Pure Logic" mode if they find the mirroring distracting.
