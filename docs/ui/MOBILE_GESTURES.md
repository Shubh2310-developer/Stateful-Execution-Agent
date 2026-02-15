# Antigravity Mobile Gestures & Interactions

The mobile experience for Antigravity is built on touch-first interactions that allow for rapid monitoring and intervention. This document defines our custom gesture library.

## 1. Core Gestures

| Gesture | Action | UI Response |
| :--- | :--- | :--- |
| **Pull to Refresh** | Global State Sync | A "Heartbeat" pulse in the status bar while syncing. |
| **Swipe Right (Task)** | Approve Checkpoint | Task card slides right with an Emerald background. |
| **Swipe Left (Task)** | Pause/Cancel | Task card slides left with an Amber/Red background. |
| **Long Press (Trace)** | Select/Copy Entry | Entry highlights and shows an action menu. |
| **Double Tap (Artifact)** | Full-screen View | Artifact Viewer expands to fill the viewport. |

## 2. Interaction Surfaces

### The Bottom Sheet
Used for complex inputs that require more space than a toast but less than a full page.
- **Expansion**: Drag handle at the top to switch between "Peek" and "Full" height.
- **Usage**: Artifact refinement, Memory editing, and Tool configuration.

### The FAB (Floating Action Button)
- **Position**: Bottom-right.
- **Function**: Primary context-aware action (e.g., "New Task" on Dashboard, "Send Feedback" on Trace view).
- **Feedback**: Haptic pulse on tap.

## 3. Navigation
- **Edge Swiping**: Support system-level edge swiping for "Back" and "Forward" navigation.
- **Tab Bar**: A fixed bottom bar for quick switching between `Dashboard`, `Active Tasks`, `Memory`, and `Alerts`.

## 4. Haptic Feedback Patterns
- **Success**: Short, light vibration.
- **Warning/Checkpoint**: Double-pulse vibration.
- **Error**: Long, heavy vibration.
- **Selection**: "Tick" haptic feedback while scrolling or moving nodes in the State Graph.

## 5. Visual Cues for Touch
- **Tap Targets**: All buttons and links must have a minimum `44x44px` area.
- **Active States**: High-contrast background shift (`bg-slate-200`) when an element is pressed.
- **Drag Indicators**: Subtle "Grab" icons or horizontal lines on components that support swiping.
