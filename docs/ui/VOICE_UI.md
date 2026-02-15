# Antigravity Voice & Natural Language UI

Voice interaction allows operators to manage Antigravity hands-free, ideal for rapid status checks or mobile "on-the-go" interventions. This document defines the speech-based UX patterns.

## 1. The "Voice of Antigravity"
- **Identity**: Consistent with the [UX Writing](./UX_WRITING.md) and [Persona Design](./PERSONA_DESIGN.md).
- **Tone**: Professional, precise, and synthesized with high-fidelity "Neural Human" characteristics.
- **Wake Word**: "Antigravity, [Goal]" or "Status check."

## 2. Verbal Status Updates
- **Progress Summaries**: "I'm 60% through the market analysis. I've found 3 key competitors and I'm currently drafting the risk section."
- **Audio Traces**: A "Narration Mode" where the agent reads out high-confidence reasoning points as they happen (optional toggle).
- **Proactive Alerts**: "Excuse me, I've hit a low-confidence decision point in the financial report. I need your input on the revenue source."

## 3. Voice Commands (Intent Mapping)
- **Goal Initiation**: "Draft a summary of the latest board meeting."
- **Status Queries**: "What is the status of task 142?" or "Is the investor update finished?"
- **Intervention**: "Pause execution," "Resume with the new data," or "Cancel that task."
- **Memory Query**: "What did you learn about my report preferences?"

## 4. Multi-modal Voice Context
- **"Look at This"**: When used in conjunction with a screen or AR, the user can say "Explain this step" or "Change that chart to a line graph," leveraging gaze or mouse position.
- **Confirmation Loop**: For high-impact actions, the agent asks for verbal confirmation: "I am about to delete the temporary artifacts. Say 'Confirm' to proceed."

## 5. Voice UX Principles
- **Conciseness**: Avoid long-winded explanations. Provide the "Bottom Line" first.
- **Barge-in Support**: Users should be able to interrupt the agent at any time.
- **Privacy Mode**: The agent only listens when the wake word is detected or the "Voice Input" button is pressed.
- **Ambient Feedback**: A subtle visual "Waveform" or pulsing logo (see [ASSETS.md](./ASSETS.md)) to indicate the agent is listening or processing.
