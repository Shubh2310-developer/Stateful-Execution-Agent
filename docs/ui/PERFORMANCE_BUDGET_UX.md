# Antigravity UI Performance Budgets

To ensure the "Professional Tool" experience, we enforce strict performance budgets for all frontend assets and interactions.

## 1. Asset Size Budgets
| Asset Type | Maximum Size (Gzipped) |
| :--- | :--- |
| **Initial Bundle** | `150 KB` |
| **Common Chunk** | `50 KB` |
| **Large Visualization (Graph)** | `100 KB` (Lazy loaded) |
| **CSS** | `20 KB` |
| **Icon Set (SVG)** | `10 KB` |

## 2. Image & Media Budgets
- **Icons**: Always SVG, max `1KB` per icon.
- **Illustrations**: Max `50KB` per SVG; use AVIF for bitmap-heavy assets.
- **Video Snippets**: Max `1MB` per snippet, always muted and looping.

## 3. Timing Budgets (The 2026 Standards)
- **TTI (Time to Interactive)**: `< 1.5s` on high-speed connection; `< 3.0s` on 4G.
- **API Response (UI Update)**: `< 200ms` for status changes.
- **Trace Entry Render**: `< 50ms` from receiving the event to it appearing in the DOM.

## 4. Resource Usage Budgets
- **CPU**: Never exceed 30% of a single core for more than 500ms (to prevent UI jank).
- **RAM**: Max `250 MB` total heap size for the browser tab.
- **Network**: Minimize polling; prefer long-lived WebSocket connections.

## 5. Monitoring & Enforcement
- **Lighthouse CI**: (See [TESTING.md](./TESTING.md)) - Block builds that exceed any budget by more than 10%.
- **Webpack Bundle Analyzer**: Mandatory review for any PR that increases the initial bundle size by more than `5 KB`.
