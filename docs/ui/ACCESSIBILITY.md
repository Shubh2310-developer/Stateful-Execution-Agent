# Antigravity UI Accessibility Guidelines

Antigravity is designed for high-stakes enterprise productivity. Accessibility is not a feature but a core requirement for ensuring all users can monitor and direct agentic work effectively.

## 1. Compliance Target
We aim for **WCAG 2.1 Level AA** compliance across all interfaces.

## 2. Color & Contrast
- **Text Contrast**: All body text and headings must maintain a minimum contrast ratio of **4.5:1** against their background.
- **Icon Contrast**: Essential icons must maintain a **3:1** ratio.
- **Color as Meaning**: Never use color as the sole indicator of status.
  - *Example*: An error status must include both a red color AND an "X" or "Warning" icon, plus a text label.

## 3. Keyboard Navigation
The interface must be fully navigable via keyboard (`Tab`, `Shift+Tab`, `Enter`, `Space`, `Esc`).
- **Focus States**: Every interactive element must have a highly visible focus ring (e.g., `outline-blue-500 offset-2`).
- **Skip Links**: A "Skip to Main Content" link must be available for keyboard users to bypass the sidebar and header.
- **Tab Order**: The tab order must follow the logical visual flow of the application (Sidebar -> Header -> Main Content -> Trace Panel).

## 4. Screen Readers & ARIA
- **Semantic HTML**: Use native elements (`<button>`, `<nav>`, `<main>`, `<aside>`) wherever possible.
- **ARIA Labels**: Use `aria-label` for icon-only buttons (e.g., the "Close Trace" button).
- **Live Regions**: The Trace Panel must use `aria-live="polite"` to announce new decision entries as they arrive without interrupting the user's current focus.
- **Alt Text**: All functional and informative images must have descriptive `alt` text. Decorative images should have `alt=""`.

## 5. Reduced Motion
We respect the user's system preference for reduced motion.
- **Implementation**: Wrap all non-essential animations in the `prefers-reduced-motion` media query.
- **Motion Effects**: Disable layout shifts, sliding panels, and pulsing animations for users with this preference.

## 6. Target Sizes
- **Clickable Area**: All buttons and interactive cards must have a minimum touch/click target of **44x44px**.
- **Spacing**: Ensure sufficient gutter space between interactive elements to prevent accidental clicks.
