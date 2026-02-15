# Antigravity UI Assets & Iconography

This document outlines the visual assets and iconography standards for the Antigravity UI.

## 1. Iconography Standards

We use a unified icon set to ensure visual consistency and professional clarity.

- **Primary Set**: [Lucide React](https://lucide.dev/) (or [Heroicons](https://heroicons.com/) for Tailwind-specific projects).
- **Style**: Outline, 2px stroke width.
- **Sizing**:
  - **Standard**: `w-5 h-5` (20px) for general UI.
  - **Large**: `w-6 h-6` (24px) for hero sections and primary navigation.
  - **Small**: `w-4 h-4` (16px) for inline metadata and status indicators.
- **Consistency**: Never mix different icon libraries. Use the same icon for the same concept across the entire application.

### Common Semantic Icons
| Concept | Icon | Usage |
|---------|------|-------|
| **Task/Goal** | `Target` | Goals and mission-level items |
| **Execution** | `Play` | Starting or running a task |
| **Trace/Log** | `Activity` | Real-time decision logs |
| **Memory** | `Brain` | Long-term learning and preferences |
| **Artifact** | `FileText` | Documents and generated outputs |
| **Success** | `CheckCircle` | Completed steps and tasks |
| **Error** | `AlertTriangle` | Failures or critical issues |
| **Settings** | `Settings` | Configuration and user profile |

## 2. Branding & Logos

The Antigravity logo represents the concept of "Stateful Autonomy" — stable but dynamic.

- **Primary Logo**: A stylized "A" using geometric lines, representing a stable foundation with an upward trajectory.
- **Color**: Primary Blue (`#3B82F6`) on light backgrounds; White on dark backgrounds.
- **Spacing**: Maintain a minimum clear space equal to 50% of the logo's height on all sides.

## 3. Visual Language

### Illustrations
- Avoid generic "AI" illustrations (brains, glowing robots).
- Prefer abstract, geometric patterns or high-quality line art that emphasizes "structure" and "process."
- Use empty-state illustrations to guide the user when no data is present.

### Logos for Third-Party Tools
- When representing external tool integrations (e.g., Slack, Groq, MongoDB), use official SVGs from [Simple Icons](https://simpleicons.org/).
- Ensure brand logos are sized consistently within the tool registry UI.

## 4. Asset Management

- **Format**: All UI icons and logos must be in **SVG** format for infinite scalability and performance.
- **Optimization**: Run all SVGs through [SVGO](https://github.com/svg/svgo) before implementation to remove metadata and minimize file size.
- **Coloring**: Use CSS `currentColor` or Tailwind text color classes (`text-slate-400`) to control icon colors rather than hardcoding hex values in the SVG files.
