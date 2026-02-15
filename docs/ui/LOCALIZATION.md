# Antigravity Localization Strategy

As a global knowledge worker, the Antigravity UI must be accessible to users across different languages and cultural contexts. This document defines our internationalization (i18n) and localization (l10n) standards.

## 1. Language Support

- **Default**: English (US).
- **Architecture**: All UI strings must be stored in translation files (e.g., `en.json`, `fr.json`) using a framework like `i18next`.
- **Dynamic Content**: The agent's reasoning (Trace entries) and generated artifacts should be localized based on the user's preference in long-term memory.

## 2. Date, Time & Numeric Formatting

- **Standardization**: Use the `Intl` browser API for all formatting.
- **Date Format**: Respect the user's locale (e.g., `MM/DD/YYYY` for US, `DD/MM/YYYY` for EU).
- **Timezones**: Always display the task's "Last Activity" in the user's local timezone, with a toggle to view in UTC for audit purposes.
- **Currency & Units**: Automatically localize currency symbols and unit measurements (metric vs. imperial) based on the user's context.

## 3. Right-to-Left (RTL) Support

- **Layout**: The interface must support RTL languages (Arabic, Hebrew) using logical CSS properties (`padding-inline-start`, `inset-inline-end`).
- **Sidebar**: Mirror the sidebar to the right side of the screen for RTL locales.
- **Icons**: Mirror directional icons (e.g., arrows) but preserve status icons (e.g., checkmarks, warning signs).

## 4. Cultural Adaptation

- **Iconography**: Ensure icons are culturally neutral. Avoid symbols that may be misinterpreted in different regions.
- **Tone & Style**: Localization is not just translation. The agent's communication style (Learned Memory) should adapt to cultural norms (e.g., formal vs. informal addressing).

## 5. UI Elasticity

- **Translation Expansion**: Design components to handle "text expansion" (some languages like German can be 30% longer than English). Use `flex-wrap` and avoided fixed widths for buttons and labels.
- **Font Selection**: Ensure the [Plus Jakarta Sans](./DESIGN_SYSTEM.md) font (or a suitable fallback) supports all required character sets (Latin, Cyrillic, CJK).
