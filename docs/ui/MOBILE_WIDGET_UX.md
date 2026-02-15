# Antigravity Mobile Widget UX

Mobile widgets provide at-a-glance monitoring of active tasks directly on the iOS or Android home screen.

## 1. Widget Sizes & Density
- **Small (2x2)**:
  - **Focus**: Single, highest-priority task.
  - **Content**: Task name, progress bar, and status icon.
- **Medium (4x2)**:
  - **Focus**: Top 3 active tasks.
  - **Content**: Goal titles and simplified trace snippets (last decision made).
- **Large (4x4)**:
  - **Focus**: Full mission overview.
  - **Content**: Active tasks, recent artifacts, and a "Quick Create" button.

## 2. Real-time Feedback
- **Live Updates**: Use iOS Live Activities or Android Dynamic Notifications for sub-minute progress updates.
- **Pulse Animation**: A subtle glow around the widget when the agent makes a "High-Impact" decision.

## 3. Widget Interactions
- **One-tap Navigation**: Tapping a task in the widget opens the app directly to that task's [Mission Control](./LAYOUTS.md).
- **Quick Approvals**: A "Checkmark" button on the widget for approving simple, low-risk checkpoints without opening the app.

## 4. Visual Style
- **Adaptive Mode**: Automatic switching between Light and Dark themes based on the system setting.
- **Consistency**: Follows the [Design Tokens](./DESIGN_TOKENS.md) for color and typography, ensuring the "Professional Tool" feel extends to the home screen.

## 5. Privacy & Security
- **Masked Data**: Sensitive artifact names or trace snippets are masked on the widget until the device is unlocked.
- **Configuration**: Long-press the widget to select which organization or team's tasks to display.
