# Antigravity CLI Design System

While the web UI is the primary interface for operators, the Antigravity CLI is the preferred tool for developers. This document defines the terminal-based visual standards.

## 1. Color Palette (ANSI)
We use standard 16-color ANSI palettes to ensure compatibility across all terminal emulators (iTerm2, VSCode, Windows Terminal).

| Role | ANSI Color | Usage |
| :--- | :--- | :--- |
| **Primary** | `Cyan` | Headers, primary labels. |
| **Secondary** | `Blue` | Secondary metadata. |
| **Success** | `Green` | Completed steps, successful validation. |
| **Warning** | `Yellow` | Checkpoints, low-confidence warnings. |
| **Error** | `Red` | Failures, critical blockers. |
| **Muted** | `Gray/Dim` | Timestamps, IDs, background info. |

## 2. Typography & Formatting
- **Headers**: Bold + Cyan.
- **Code Snippets**: Inverted background or dedicated border.
- **Tables**: Use `cli-table3` or equivalent for clean, bordered layouts.
- **Emphasis**: Use *Italics* sparingly (some terminals don't support it); prefer Bold.

## 3. Progress Indicators
- **Step Loading**: A rotating spinner (e.g., `⠋`, `⠙`, `⠹`, `⠸`) with the active step label.
- **Task Progress**: A high-density progress bar: `[====>    ] 40%`.
- **Streaming Trace**: Append-only log entries with a consistent prefix: `[REASONING] Searching docs...`.

## 4. Iconography (Unicode/Nerd Fonts)
Use standard Unicode symbols for status:
- `✔` Success
- `✖` Error
- `⚠` Warning
- `➜` Action/Handoff
- `💡` Insight/Memory

## 5. Interaction Patterns
- **Prompts**: Clear, bold questions followed by a colored input cursor.
- **Selection**: Use arrow keys to navigate lists with the active item highlighted in Cyan.
- **Clear Screen**: Use `cls` or `clear` patterns to maintain a tidy terminal during state transitions.
