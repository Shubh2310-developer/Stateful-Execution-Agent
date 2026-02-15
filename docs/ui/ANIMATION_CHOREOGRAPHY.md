# Antigravity Animation Choreography

Choreography defines how multiple UI elements move in relation to each other, creating a sense of hierarchy, flow, and professional "polish." This document outlines the choreographed motion sequences for the Antigravity UI.

## 1. Page Transition Choreography
When navigating between high-level views (e.g., Dashboard -> Mission Control):
1. **Existing Content**: Fades out and scales down slightly (`scale-95`) over `150ms`.
2. **Global Navigation (Sidebar/Header)**: Remains static to provide a "Stable Frame."
3. **New Content**: Fades in and scales up from `scale-105` over `300ms` with a staggered entry for sub-components (stagger: `50ms` per card/panel).

## 2. Mission Control Activation
When a task is launched and the workspace transitions to the active monitoring state:
1. **The Pulse**: The status bar in the header begins its "Heartbeat" animation.
2. **Sidebar**: Collapses to icon-only mode over `300ms`.
3. **Center Workplace**: Slides up from the bottom with an `overshoot` ease.
4. **The Trace Panel**: Slides in from the right, appearing last to signal that the agent's "Thinking" has begun.

## 3. Decision Trace Stagger
As new entries arrive in the Decision Trace:
1. **New Entry**: Appears at the bottom (or top depending on sort) with a `0` height, expanding to full height over `250ms`.
2. **Sub-elements**: The "Decision Point," "Reasoning," and "Confidence Score" fade in sequentially with a `100ms` stagger between them.
3. **Ghost Loading**: While the agent is "Thinking," a skeleton version of the next card is visible with a "Shimmer" effect.

## 4. State Graph (DAG) Evolution
When the execution plan changes or a step completes:
1. **Completed Node**: Transitions from Blue Pulse to Solid Emerald. A "Check" icon animates in using a scale-pop effect.
2. **Edges (Connectors)**: Animate a "Data Pulse" (a small glowing dot) moving from the completed node to the next active node.
3. **Zoom/Pan**: If the active node is outside the current viewport, the camera smoothly pans to center the node over `500ms`.

## 5. Artifact Transformation
When a step produces an artifact that is then used by a subsequent step:
1. **Output Creation**: A small "Artifact Card" pops out of the active step node.
2. **Traversal**: The card moves along the graph edge to the next step's input slot.
3. **Absorption**: The card fades into the next step, signaling that the data has been successfully handed off.

## 6. Feedback & Correction Loops
When a user clicks "Refine":
1. **Current Artifact**: Dims to 50% opacity.
2. **Refinement Input**: Slides up from the bottom of the Workplace, pushing the artifact preview up slightly.
3. **Ghost Preview**: As the user types, the agent shows "Ghost Text" in the artifact area, visualizing the planned changes in real-time.
