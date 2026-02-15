# Antigravity Design System

This document specifies the visual foundations for the Antigravity UI, optimized for professional enterprise productivity in 2026.

## 🎨 Color Palette

We use a high-contrast, functional color system. Colors are used to indicate status, priority, and focus.

### Core Colors
| Role | Hex | Tailwind Class | Usage |
|------|-----|----------------|-------|
| **Primary** | `#3B82F6` | `bg-blue-600` | Primary actions, active states |
| **Secondary** | `#60A5FA` | `bg-blue-400` | Muted actions, secondary indicators |
| **CTA** | `#F97316` | `bg-orange-500` | Critical conversion points, highlights |
| **Background** | `#F8FAFC` | `bg-slate-50` | Primary application surface |
| **Surface** | `#FFFFFF` | `bg-white` | Cards, modals, sidebars |
| **Text** | `#1E293B` | `text-slate-900` | Body text, headings |
| **Muted** | `#64748B` | `text-slate-500` | Secondary text, metadata |

### Status Colors
| Status | Hex | Tailwind Class |
|--------|-----|----------------|
| **Success** | `#10B981` | `text-emerald-500` |
| **Warning** | `#F59E0B` | `text-amber-500` |
| **Error** | `#EF4444` | `text-red-500` |
| **Info/Pending** | `#6366F1` | `text-indigo-500` |

## Typography

**Font Family**: `Plus Jakarta Sans`
Precision-focused, modern sans-serif with excellent readability at small sizes.

### Font Scales
| Level | Size | Weight | Line Height |
|-------|------|--------|-------------|
| **H1** | `2.25rem` (36px) | 700 | 1.2 |
| **H2** | `1.5rem` (24px) | 600 | 1.3 |
| **H3** | `1.125rem` (18px) | 600 | 1.4 |
| **Body** | `1rem` (16px) | 400 | 1.6 |
| **Small** | `0.875rem` (14px) | 400 | 1.5 |
| **Code** | `0.875rem` (14px) | 400 | 1.5 |

## 🏗️ Layout & Grids

- **Max Width**: `max-w-7xl` (1280px) for general content.
- **Sidebar**: Fixed `280px` for primary navigation.
- **Trace Panel**: Right-side collapsible `400px` for decision logs.
- **Spacing Scale**: Tailwind-standard `4px` increments (`p-4`, `m-8`, etc.).

## ✨ Effects & Styling

- **Flat Design**: No heavy shadows. Use `1px` borders (`border-slate-200`) for depth.
- **Borders**: `rounded-lg` (8px) for cards, `rounded-full` for status pills.
- **Hover**: Subtle background shifts (`bg-slate-100`) or opacity changes.
- **Transitions**: `150ms-200ms` ease-in-out for all interactive states.
