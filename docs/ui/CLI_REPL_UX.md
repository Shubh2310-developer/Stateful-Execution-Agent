# Antigravity CLI Interactive Mode (REPL)

The Antigravity CLI provides a high-performance Read-Eval-Print Loop (REPL) for developers. This document defines the interaction patterns for this terminal-based interface.

## 1. The Prompt Surface
- **Identity**: The prompt is prefixed with the Antigravity logo (in ANSI color) and the current state: `(main) ➜ antigravity > `.
- **Auto-completion**: Tab-completion for commands, task IDs, and available tools.
- **Syntax Highlighting**: Real-time coloring of commands and JSON inputs.

## 2. Command Palette (CLI version)
- **Shortcuts**: Use `/` for commands and `?` for help.
- **Fuzzy Search**: A popup-style list within the terminal for searching history or tools.

## 3. Streaming Reasoning
- **Log Levels**: Toggles to see `VERBOSE` (full trace), `INFO` (high-level steps), or `SILENT` (artifacts only).
- **Live Updating**: Using terminal "rewriting" (ANSI escape codes) to update progress bars and step status in-place without scrolling the terminal.

## 4. Artifact Handling
- **`cat` and `less` Patterns**: Commands to render generated Markdown or JSON directly in the terminal with proper formatting.
- **`open` Integration**: Automatically open generated PDFs or charts in the user's default system viewer.

## 5. State Management
- **`state save/load`**: Commands to manually snapshot or restore the agent's state from the terminal.
- **History Navigation**: Use `Up/Down` arrows to navigate previous goals and `Ctrl+R` to search the task history.
