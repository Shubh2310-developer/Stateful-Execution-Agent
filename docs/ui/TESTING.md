# Antigravity UI Testing Strategy

To maintain high quality in a professional agentic UI, we employ a multi-layered testing strategy that covers visual consistency, functional correctness, and accessibility.

## 1. Visual Regression Testing
Ensure that design system changes don't cause unintended side effects across the application.
- **Tool**: [Playwright](https://playwright.dev/) with `toHaveScreenshot`.
- **Target**: Atomic components (`Button`, `Pill`) and molecular components (`TaskCard`, `TraceEntry`).
- **Modes**: Test both Light and Dark modes.

## 2. Component Unit Testing
Validate the logic and rendering of individual components.
- **Tool**: [Vitest](https://vitest.dev/) + [React Testing Library](https://testing-library.com/docs/react-testing-library/intro/).
- **Coverage**: Focus on state-driven rendering (e.g., "Does the Progress Bar show the correct percentage?") and event handling (e.g., "Does clicking 'View Trace' call the correct navigation function?").

## 3. Integration & E2E Testing
Validate the end-to-end task execution flow, including real-time updates.
- **Tool**: Playwright.
- **Scenarios**:
  - Task Creation -> Plan Generation -> Execution Start.
  - Handling a real-time Trace Event update.
  - Responding to a "Needs Review" checkpoint.
  - Successfully downloading a generated artifact.

## 4. Accessibility (a11y) Testing
Ensure compliance with WCAG 2.1 Level AA.
- **Automated**: [axe-core](https://www.deque.com/axe/) integration in Playwright/Vitest.
- **Manual**:
  - Keyboard-only navigation audit.
  - Screen reader walkthrough (VoiceOver/NVDA).
  - Contrast checks using dev tools.

## 5. UI Performance Benchmarking
Monitor client-side performance against our [Performance Targets](./PERFORMANCE.md).
- **Tool**: [Lighthouse CI](https://github.com/GoogleChrome/lighthouse-ci).
- **Metrics**: LCP, FID, CLS, and Total Blocking Time.
- **CI/CD**: Block merges if Lighthouse scores drop below the 95 threshold.

## 6. Edge Case Testing
- **Network Latency**: Test UI behavior under high latency (3G simulation) to ensure skeleton screens and loading states function correctly.
- **Extreme Data Density**: Test the Trace Panel with 5,000+ entries to validate virtualization performance.
- **Invalid State**: Ensure the UI handles malformed or missing backend data without crashing (using Error Boundaries).
