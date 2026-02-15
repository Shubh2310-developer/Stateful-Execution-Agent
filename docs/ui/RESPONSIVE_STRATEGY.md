# Antigravity Responsive Strategy

The Antigravity UI is a professional-grade operational tool. It must provide a seamless experience across desktop, tablet, and mobile, adapting its information density to the device's constraints.

## 1. Breakpoints

We use standard Tailwind CSS breakpoints, optimized for 2026 device standards:

| Breakpoint | Width | Target Devices |
|------------|-------|----------------|
| **xs** | `375px` | Compact Mobile |
| **sm** | `640px` | Large Mobile / Small Tablets |
| **md** | `768px` | Tablets (Portrait) |
| **lg** | `1024px` | Tablets (Landscape) / Small Laptops |
| **xl** | `1280px` | Standard Desktops |
| **2xl** | `1536px` | Large Monitors / High-Res Displays |

## 2. Adaptive Information Density

- **Desktop (xl+)**: Maximum density. Sidebars and Trace panels are fixed and visible. Full task trees are displayed.
- **Tablet (md - lg)**: Selective density. The Trace panel becomes a slide-over or a separate tab. Grids transition from 3 columns to 2.
- **Mobile (xs - sm)**: Essential density. Single-column layout. Focus on task status and immediate feedback. The Trace is accessible via a bottom sheet or a dedicated view.

## 3. Layout Adaptation Patterns

### Sidebar
- **Desktop**: Fixed left.
- **Mobile**: Collapsed into a "Hamburger" menu or a bottom navigation bar for quick access to "Tasks" and "Alerts."

### The Trace Panel
- **Desktop**: Persistent right column.
- **Mobile**: Collapsed into a floating action button (FAB) that opens a full-screen overlay when the agent is active.

### Data Tables
- **Desktop**: Full multi-column tables with sorting and filtering.
- **Mobile**: Card-based lists showing only the most critical fields (e.g., Task Name, Status, Last Update).

## 4. Input & Interaction
- **Touch Targets**: Minimum `44x44px` on all mobile/tablet views.
- **Gestures**: Support swipe-to-dismiss for notifications and pull-to-refresh for task lists on mobile.
- **Hover States**: Gracefully degrade hover effects on touch devices; use active states instead.

## 5. Performance for Mobile
- **Image Optimization**: Use responsive images (`srcset`) and WebP/AVIF formats.
- **Lazy Loading**: Defer the loading of complex visualizations (like the State DAG) until they enter the viewport.
- **Font Rendering**: Use `font-display: swap` to ensure text is readable immediately.
