# Antigravity Grid & Spacing Math

Precision is a core tenet of the Antigravity UI. This document defines the mathematical grid system and spacing scales used to ensure a perfectly aligned, "app-like" experience.

## 1. The 4px Base Unit
All spacing, sizing, and typography line heights are derived from a **4px** base unit.

- **1 unit**: `4px` (`0.25rem`)
- **2 units**: `8px` (`0.5rem`)
- **4 units**: `16px` (`1rem`) - *Standard Base*
- **6 units**: `24px` (`1.5rem`)
- **8 units**: `32px` (`2rem`)

## 2. Spacing Scale (Tailwind)

| Scale | Value | Usage |
| :--- | :--- | :--- |
| `0.5` | `2px` | Minimal separators, thin borders. |
| `1` | `4px` | Tight groupings, icon-to-text gaps. |
| `2` | `8px` | Secondary padding, small component margins. |
| `4` | `16px` | Standard container padding, gutter spacing. |
| `6` | `24px` | Card padding, large component separation. |
| `8` | `32px` | Section margins, header-to-content spacing. |
| `12` | `48px` | Hero section padding, empty state centering. |

## 3. Layout Grid (Desktop)

- **Total Columns**: 12-column grid system for the Main Workplace.
- **Gutter Width**: `24px` (`gap-6`).
- **Sidebar Width**: Fixed `280px`.
- **Trace Panel Width**: Fixed `400px` (when expanded).
- **Container Max-Widths**:
  - `xl`: `1280px`
  - `2xl`: `1536px`

## 4. Layout Math & Alignment

- **Vertical Alignment**: All text must align to the top or center of the 4px grid.
- **Header Height**: Fixed `64px` (`h-16`).
- **Input Height**: Standard `40px` (`h-10`) or Large `48px` (`h-12`).
- **Border Radius**:
  - `8px` (`rounded-lg`) for primary cards and buttons.
  - `12px` (`rounded-xl`) for main application panels and modals.
  - `9999px` (`rounded-full`) for status pills and avatars.

## 5. Information Density Rules

- **Comfortable**: `p-6` (24px) padding between elements.
- **Compact**: `p-3` (12px) padding between elements.
- **Subgrid**: Use CSS Subgrid for nested components (like the "Steps" list within a Task Card) to ensure they align to the parent's 12-column grid.
