/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./ui/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // Semantic Mapping to CSS Variables
        background: {
          DEFAULT: 'var(--color-bg-base)',
          surface: 'var(--color-bg-surface)',
          muted: 'var(--color-bg-muted)',
          dark: 'var(--color-bg-dark)',
          well: 'var(--color-bg-well)',
        },
        text: {
          primary: 'var(--color-text-primary)',
          secondary: 'var(--color-text-secondary)',
          muted: 'var(--color-text-muted)',
          'on-dark': 'var(--color-text-on-dark)',
        },
        brand: {
          primary: 'var(--color-brand-primary)',
          cta: 'var(--color-brand-cta)',
        },
        status: {
          success: 'var(--color-status-success)',
          warning: 'var(--color-status-warning)',
          error: 'var(--color-status-error)',
          info: 'var(--color-status-info)',
        },
        // Legacy/Direct mappings from DESIGN_SYSTEM.md
        primary: '#3B82F6',
        secondary: '#60A5FA',
        cta: '#F97316',
      },
      fontFamily: {
        sans: ['"Plus Jakarta Sans"', 'ui-sans-serif', 'system-ui'],
        mono: ['"JetBrains Mono"', 'ui-monospace', 'SFMono-Regular'],
      },
      spacing: {
        'ant-1': '4px',
        'ant-2': '8px',
        'ant-4': '16px',
        'ant-6': '24px',
        'ant-8': '32px',
        'ant-12': '48px',
        'sidebar': '280px',
        'trace': '400px',
        'header': '64px',
      },
      borderRadius: {
        'ant-sm': 'var(--radius-sm)',
        'ant-md': 'var(--radius-md)',
        'ant-lg': 'var(--radius-lg)',
      },
      transitionDuration: {
        'DEFAULT': '200ms',
        'fast': '150ms',
        'standard': '300ms',
        'deliberate': '500ms',
      },
      transitionTimingFunction: {
        'ease-out-ant': 'cubic-bezier(0, 0, 0.2, 1)',
        'ease-in-out-ant': 'cubic-bezier(0.4, 0, 0.2, 1)',
        'quart-out': 'cubic-bezier(0.16, 1, 0.3, 1)',
      },
      maxWidth: {
        '7xl': '1280px',
      }
    },
  },
  plugins: [],
}
