# Antigravity Design Tokens

Design Tokens are the "Source of Truth" for all visual properties in the Antigravity UI. They bridge the gap between design specs and frontend implementation.

## 1. Color Tokens

### Backgrounds
- `color-bg-base`: `#F8FAFC` (Slate-50)
- `color-bg-surface`: `#FFFFFF` (White)
- `color-bg-muted`: `#F1F5F9` (Slate-100)
- `color-bg-dark`: `#0F172A` (Slate-900)

### Text
- `color-text-primary`: `#1E293B` (Slate-900)
- `color-text-secondary`: `#475569` (Slate-600)
- `color-text-muted`: `#94A3B8` (Slate-400)
- `color-text-on-dark`: `#F8FAFC` (Slate-50)

### Brand & Status
- `color-brand-primary`: `#3B82F6` (Blue-600)
- `color-brand-cta`: `#F97316` (Orange-500)
- `color-status-success`: `#10B981` (Emerald-500)
- `color-status-warning`: `#F59E0B` (Amber-500)
- `color-status-error`: `#EF4444` (Red-500)

## 2. Typography Tokens

- `font-family-sans`: `"Plus Jakarta Sans", sans-serif`
- `font-family-mono`: `"JetBrains Mono", monospace`

### Sizes
- `font-size-xs`: `0.75rem` (12px)
- `font-size-sm`: `0.875rem` (14px)
- `font-size-base`: `1rem` (16px)
- `font-size-lg`: `1.125rem` (18px)
- `font-size-xl`: `1.5rem` (24px)
- `font-size-2xl`: `2.25rem` (36px)

## 3. Spacing Tokens

- `spacing-base`: `4px`
- `spacing-1`: `4px`
- `spacing-2`: `8px`
- `spacing-4`: `16px`
- `spacing-6`: `24px`
- `spacing-8`: `32px`

## 4. Radius Tokens

- `radius-sm`: `4px`
- `radius-md`: `8px`
- `radius-lg`: `12px`
- `radius-full`: `9999px`

## 5. Shadow Tokens (Subtle)

- `shadow-sm`: `0 1px 2px 0 rgb(0 0 0 / 0.05)`
- `shadow-md`: `0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)`

## 6. Implementation (Tailwind Example)

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        'antigravity-blue': 'var(--color-brand-primary)',
        'antigravity-orange': 'var(--color-brand-cta)',
      },
      spacing: {
        'ant-4': '16px',
        'ant-6': '24px',
      }
    }
  }
}
```
