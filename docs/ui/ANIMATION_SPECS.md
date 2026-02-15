# Antigravity Animation & Motion Specifications

This document defines the technical easing functions, durations, and motion patterns for the Antigravity UI. We use a "Weighted Utility" motion profile: fast, purposeful, and stable.

## 1. Timing Durations

| Category | Duration | Tailwind Class | Usage |
| :--- | :--- | :--- | :--- |
| **Instant** | `75ms` | `duration-75` | Subtle opacity shifts, icon hovers. |
| **Fast** | `150ms` | `duration-150` | Standard button transitions, checkbox toggles. |
| **Standard** | `300ms` | `duration-300` | Accordion expansion, modal entry, sidebar toggle. |
| **Deliberate** | `500ms` | `duration-500` | Large panel entries, complex DAG transitions. |

## 2. Easing Functions

We use standard CSS bezier curves that prioritize a fast start and a smooth finish.

- **Ease-Out (Standard)**: `cubic-bezier(0, 0, 0.2, 1)`
  - Used for elements entering the screen or responding to user input.
- **Ease-In-Out (Smooth)**: `cubic-bezier(0.4, 0, 0.2, 1)`
  - Used for background color shifts and continuous transitions.
- **Linear**: `linear`
  - Only used for the "Running" pulse animation or progress bars.

## 3. Core Motion Patterns

### 3.1 The "Lift" (Hover)
When a user hovers over a Task Card or Artifact:
- **Transform**: `translateY(-2px)`
- **Duration**: `200ms`
- **Easing**: `ease-out`
- **Effect**: Subtle elevation to indicate interactivity.

### 3.2 The "Slide-In" (Panels)
When the Trace Panel or a Modal opens:
- **Starting State**: `translateX(100%)` (for Right Panel) or `scale(0.95)` (for Modal).
- **Ending State**: `translateX(0)` or `scale(1)`.
- **Duration**: `300ms`
- **Easing**: `cubic-bezier(0.16, 1, 0.3, 1)` (Quart-Out).

### 3.3 The "Pulse" (Status)
For the "Running" state indicator:
- **Animation**: `pulse`
- **Opacity Range**: `0.4` to `1.0`.
- **Frequency**: `2000ms` per cycle.

### 3.4 The "Flow" (Graph Transitions)
When the State Visualization graph updates:
- **Nodes**: Cross-fade opacity over `300ms`.
- **Edges**: Use a drawing animation (SVG `stroke-dashoffset`) over `500ms` to show data flow direction.

## 4. Performance & Accessibility

- **GPU Acceleration**: Always use `transform` and `opacity` for animations. Avoid animating `width`, `height`, or `margin` to prevent layout reflows.
- **Hardware Rendering**: Apply `will-change: transform` to the Trace Panel and State Canvas to ensure smooth scrolling.
- **Reduced Motion**: If `prefers-reduced-motion: reduce` is detected:
  - Disable all `translate` and `scale` transforms.
  - Convert `slide-in` to a simple `opacity` fade.
  - Disable the `pulse` animation on status indicators.
