# Antigravity Accessibility (a11y) Checklist

Use this checklist during the design, development, and QA phases to ensure Antigravity meets WCAG 2.1 Level AA compliance.

## 1. Perceivable

- [ ] **Contrast**: Check that all text has a contrast ratio of at least 4.5:1.
- [ ] **Non-text Content**: All icons, images, and charts have descriptive `alt` text or `aria-labels`.
- [ ] **Status Indicators**: Color is not the only way status is conveyed (e.g., Error has both red text and an icon).
- [ ] **Structure**: Use semantic headings (H1-H3) in logical order.
- [ ] **Dark Mode**: High-contrast theme maintained for users with visual impairments.

## 2. Operable

- [ ] **Keyboard Nav**: The entire application can be navigated using only the keyboard (`Tab`, `Space`, `Enter`).
- [ ] **Focus Visible**: All interactive elements have a clear, high-contrast focus ring.
- [ ] **Skip Links**: "Skip to Main Content" is present and functional.
- [ ] **Timing**: No time-limited tasks. If an agent times out, the user is notified without loss of data.
- [ ] **Reduced Motion**: All animations are disabled or simplified if the user prefers reduced motion.
- [ ] **Target Size**: All buttons and links have a minimum clickable area of 44x44px.

## 3. Understandable

- [ ] **Language**: Page language is set in the HTML tag (`lang="en"`).
- [ ] **Consistency**: Navigation and icons are consistent across all views.
- [ ] **Input Validation**: All forms have clear labels and real-time error messages that are announced by screen readers.
- [ ] **Terminology**: Specialized AI terms are explained in the [Glossary](./GLOSSARY.md) or via tooltips.

## 4. Robust

- [ ] **ARIA Landmarks**: Use `role="main"`, `role="navigation"`, `role="complementary"` (for Trace Panel).
- [ ] **Live Regions**: Decision Trace entries use `aria-live="polite"`.
- [ ] **Screen Reader Testing**: Walk through the "Task Creation" and "Review" journeys using VoiceOver (Mac/iOS) or NVDA (Windows).
- [ ] **Browser Support**: Interface remains functional on all modern browsers (Chrome, Firefox, Safari, Edge).

## 5. AI-Specific Checklist

- [ ] **Uncertainty Disclosure**: Low-confidence decisions are clearly flagged.
- [ ] **Verification**: Users can always verify an agent's reasoning via the Decision Trace.
- [ ] **Control**: High-impact actions require explicit manual approval.
- [ ] **Rollback**: Users can easily undo or rollback agent actions via the State Versioning UI.
