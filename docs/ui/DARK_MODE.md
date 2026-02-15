# Antigravity Dark Mode Specification

This document defines the high-contrast professional dark theme for the Antigravity UI, optimized for developers and long-session monitoring in 2026.

## 🌙 Dark Theme Philosophy

Our dark mode is not just an inverted light mode. It is a specialized environment designed to:
1. **Reduce Eye Strain**: Utilizing deep slates rather than pure blacks.
2. **Maintain Functional Depth**: Using layering and borders rather than heavy shadows.
3. **Enhance Traceability**: Using vibrant (but not neon) status colors to draw attention to agent activity.

## 🎨 Color Palette (Dark)

### Surface Colors
| Role | Hex | Tailwind Class | Usage |
|------|-----|----------------|-------|
| **Background** | `#0F172A` | `bg-slate-900` | Primary application background |
| **Surface** | `#1E293B` | `bg-slate-800` | Cards, sidebar, panel backgrounds |
| **Elevated** | `#334155` | `bg-slate-700` | Hover states, active items |
| **Border** | `#1E293B` | `border-slate-800` | Default separators |
| **Border Subtle**| `#334155` | `border-slate-700` | Interactive element borders |

### Text Colors
| Role | Hex | Tailwind Class | Usage |
|------|-----|----------------|-------|
| **Primary** | `#F8FAFC` | `text-slate-50` | Headings, primary content |
| **Secondary** | `#CBD5E1` | `text-slate-300` | Body text, readable content |
| **Muted** | `#94A3B8` | `text-slate-400` | Metadata, disabled states |

## ✨ Status Colors (Dark)
Status colors are adjusted for optimal vibrance and contrast against dark backgrounds.

| Status | Hex | Tailwind Class |
|--------|-----|----------------|
| **Success** | `#34D399` | `text-emerald-400` |
| **Warning** | `#FBBF24` | `text-amber-400` |
| **Error** | `#F87171` | `text-red-400` |
| **Info/Pending**| `#818CF8` | `text-indigo-400` |

## 🏗️ Layering and Depth

In dark mode, depth is created by moving "up" the slate scale:
- **Level 0 (Base)**: `bg-slate-950` (The "well" for the workspace)
- **Level 1 (App)**: `bg-slate-900` (Main navigation and header)
- **Level 2 (Content)**: `bg-slate-800` (Task cards and trace entries)
- **Level 3 (Interactive)**: `bg-slate-700` (Hovered cards and tooltips)

## 🎨 Glassmorphism (Optional Accent)
For the Trace Panel and specialized overlays, use a controlled glass effect:
- **Background**: `bg-slate-900/80`
- **Blur**: `backdrop-blur-md`
- **Border**: `border-white/10`

## ⌨️ Code & Trace Views
- **Code Background**: `#111827` (slate-950)
- **Syntax Highlighting**: Prefer the **Vitesse Dark** or **One Dark Pro** color schemes for consistent technical aesthetics.
- **Trace Selection**: Active trace entries should use a `border-l-blue-500` and a `bg-blue-500/10` highlight.
