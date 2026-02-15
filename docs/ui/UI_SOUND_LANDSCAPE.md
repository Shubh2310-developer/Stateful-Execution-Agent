# Antigravity UI Sound Landscape (Earcons)

Sound provides a non-visual feedback layer, essential for heads-down productivity and situational awareness. We use a "Minimalist Harmonic" audio palette.

## 1. Audio Philosophy
- **Non-intrusive**: Short durations (< 300ms) with soft attack/decay.
- **Informative**: Different frequencies and timbres represent different states.
- **Spatial Aware**: Sound directionality mirrors the UI layout (e.g., Trace sounds come from the right).

## 2. Semantic Sound Lexicon (Earcons)

| Event | Audio Character | Pitch | Meaning |
| :--- | :--- | :--- | :--- |
| **Task Start** | Rising harmonic | Low to Mid | Upward momentum. |
| **Step Success** | High-pitch 'chime' | High | Accomplishment/Positive. |
| **Checkpoint** | Soft 'double-pulse' | Mid | Attention required (non-urgent). |
| **Memory Saved** | Sub-bass 'thump' | Low | Stable foundation/Learning. |
| **Error** | Dissonant 'chord' | Low | Friction/Intervention needed. |
| **Completion** | Sustained 'chord' | High | Success/Goal reached. |

## 3. Ambient Textures
- **The "Reasoning Hum"**: A very low-volume, oscillating tone that persists while the agent is "Thinking," providing a subconscious signal that the system is active.
- **Data Stream Shimmer**: A granular audio texture when large artifacts are being generated or transferred.

## 4. Audio-UI Sync
- **Animation Sync**: Sounds are triggered at the *peak* of their associated visual animation (e.g., as a status pill turns Emerald).
- **Haptic Sync**: (See [HAPTIC_LANGUAGE_SPECS.md](./HAPTIC_LANGUAGE_SPECS.md)) - Audio and tactile feedback should be perfectly synchronized.

## 5. User Controls
- **Audio Themes**: "Classic Digital," "Natural Acoustic," "Cybernetic Industrial."
- **Volume Toggles**: Granular volume for "Alerts," "Ambience," and "Success Cues."
- **Silent Mode**: Full audio mute with a visual indicator in the status bar.
