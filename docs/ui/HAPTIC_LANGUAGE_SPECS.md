# Antigravity Haptic Language Specifications

Haptics provide a tactile dimension to agent monitoring, allowing operators to "feel" the state of the swarm without looking at a screen.

## 1. Tactile Lexicon

| Event | Haptic Pattern | Intensity | Usage |
| :--- | :--- | :--- | :--- |
| **Step Start** | Short 'click' (30ms) | Low | Subtle confirmation of progress. |
| **Step Success** | Double 'pop' (50ms/50ms) | Medium | Positive reinforcement. |
| **Checkpoint** | Pulsing 'throb' (500ms) | High | Urgency for user input. |
| **Tool Execution** | Continuous 'hum' | Varying | Pitch increases with latency. |
| **Memory Saved** | Soft 'whisper' (100ms fade) | Low | Confirmation of learning. |
| **Critical Error** | Heavy 'jolt' (200ms) | Max | Immediate intervention required. |

## 2. Swarm Density Haptics
- **Activity Texture**: A "Roughness" or "Granularity" felt through a trackpad or haptic controller that reflects the number of active agents in a swarm.
- **Flow Direction**: A directional "swipe" feel that indicates if data is being pushed to an external tool or pulled from a source.

## 3. Reasoning "Friction"
- **Uncertainty Feedback**: Increased tactile resistance when scrolling through a Decision Trace entry with low confidence.
- **Logical Alignment**: A "Magnetic Snap" feel when the user's manual correction aligns perfectly with the agent's secondary path.

## 4. Device-specific Implementation
- **Mobile**: Utilizing the Taptic Engine (iOS) or Haptic Feedback (Android).
- **Spatial/VR**: (See [VR_WORKSPACE_UX.md](./VR_WORKSPACE_UX.md)) - Using haptic gloves or vests for full-body situational awareness.
- **Desktop**: Specialized haptic mice or trackpads.

## 5. Customization
- **Tactile Themes**: Allow users to choose different "Feel Profiles" (e.g., "Minimalist Clicky," "Smooth Organic," "Technical Industrial").
- **Accessibility**: Support for "Haptic Only" modes for users with visual impairments.
