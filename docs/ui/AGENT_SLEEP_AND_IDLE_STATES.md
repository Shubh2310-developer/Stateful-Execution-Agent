# Antigravity Agent Idle & Sleep States

Autonomous agents aren't always active. This document defines the UI patterns for when the agent is waiting, idling, or in a low-power "Sleep" state.

## 1. The Idle "Pulse"
- **Visual**: The agent avatar (see [PERSONA_DESIGN.md](./PERSONA_DESIGN.md)) transitions to a slow, dim "Breathing" animation.
- **Status Label**: "Awaiting Input" or "Monitoring Environment."
- **Idle Reasoning**: Subtle indicators that the agent is still "thinking" or "watching" even if it's not executing (e.g., "Observing Slack for mentions...").

## 2. Deep Sleep Mode
- **Visual**: The UI drapes in a translucent "Sleeping" overlay or shifts the color temperature to deep indigo.
- **Wake Conditions**: Clearly display what will wake the agent (e.g., "Wakes at 9:00 AM UTC" or "Wakes on API Webhook").
- **Manual Wake**: A prominent, high-contrast "Wake Agent" button.

## 3. "Daydreaming" (Low-Priority Optimization)
- **Background Tasks**: While idle, the agent may perform low-priority cleanup, memory indexing, or ROI calculation.
- **Visual**: Muted, secondary "Background Pulse" in the status bar.
- **Impact**: "While idle, I've consolidated 5 new memory patterns."

## 4. Latency-induced Idle
- **Waiting for API**: If a third-party tool is slow, the agent shows a "Waiting for [Tool Name]" state with a live timer.
- **Retrying Animation**: A "Revolving" icon around the agent's avatar to signal a loop in a transient failure state.

## 5. Transition Choreography
- **Waking Up**: The UI "Brightens" and panels expand from the center as the agent restores its active context.
- **Going to Sleep**: Panels collapse and colors dim, with a "State Snapshot Saved" confirmation toast.
