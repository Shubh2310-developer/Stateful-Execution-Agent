# Antigravity Command Palette (Keyboard Efficiency)

For power users and operators, the Command Palette (`Cmd+K` or `Ctrl+K`) is the primary interface for high-speed agent management. This document defines the UI/UX patterns for this keyboard-centric interaction.

## 1. Visual Design

- **Overlay**: A centered, modal-like overlay with a subtle backdrop blur (`backdrop-blur-md`).
- **Typography**: Large, high-contrast input text with a fixed-width font for commands.
- **Results**: A list of actionable items with keyboard shortcuts (`Enter` to select, `Arrow Keys` to navigate).
- **Style**: Polished Flat Design, consistent with the [Design System](./DESIGN_SYSTEM.md).

## 2. Core Command Patterns

### Task Management
- `/new`: Initiate a new task goal.
- `/pause`: Pause the current active task.
- `/resume`: List paused tasks to resume.
- `/cancel`: Terminate the current execution.

### Navigation
- `> Dashboard`: Jump to the main overview.
- `> Memory`: Open the memory management view.
- `> Trace`: Focus the Decision Trace panel.
- `> Settings`: Open configuration.

### Agent Control
- `! restart step`: Re-run the current plan step.
- `! modify plan`: Open the plan editor.
- `! clear memory`: Flush the current short-term context.

## 3. Real-time Search Integration

The Command Palette acts as a global search for the entire system:
- **Tasks**: Search by goal name or ID.
- **Artifacts**: Search by filename or content keywords.
- **Memory**: Search for learned facts or preferences.
- **Tools**: Search for available tools and their capabilities.

## 4. Interaction States

- **Fuzzy Matching**: Commands and search results should use fuzzy matching for high-speed entry.
- **Recent Actions**: Display the last 3 actions at the top of the palette when opened.
- **Loading States**: If a search is async, show a minimalist shimmer or a "Scanning..." indicator in the results area.

## 5. Implementation Notes

- **Library**: Use a robust library like [KBAR](https://kbar.vercel.app/) or [CommandBar](https://www.commandbar.com/) for React implementations.
- **Focus Management**: Ensure focus is automatically moved to the input on open and restored to the previous element on close.
- **Accessibility**: Support ARIA roles for listboxes and ensure all commands are announced by screen readers.
