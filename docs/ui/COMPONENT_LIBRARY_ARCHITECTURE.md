# Antigravity Component Library Architecture

To ensure speed and consistency, the Antigravity UI is built on a modular component architecture. This document defines how components are organized and implemented.

## 1. Organization Pattern (Atomic Design Lite)

Components are organized into four tiers:

- **Tier 1: Atoms** (UI/Primitives): Basic building blocks with no internal logic.
  - *Examples*: `Button`, `Input`, `Badge`, `Pill`, `Icon`.
  - *Location*: `src/components/ui/`
- **Tier 2: Molecules** (Functional): Combinations of atoms that serve a specific UI purpose.
  - *Examples*: `TaskCard`, `TraceEntry`, `ArtifactPreview`.
  - *Location*: `src/components/shared/`
- **Tier 3: Organisms** (Feature-scoped): Complex units with internal state or API hooks.
  - *Examples*: `DecisionTraceStream`, `StateGraphCanvas`, `MemoryEditor`.
  - *Location*: `src/features/[feature-name]/components/`
- **Tier 4: Layouts**: Page-level structures that arrange organisms.
  - *Examples*: `MissionControlLayout`, `DashboardGrid`.
  - *Location*: `src/layouts/`

## 2. Implementation Standards

- **React + TypeScript**: All components must have strictly typed props.
- **Tailwind CSS**: Use utility classes for styling. Avoid custom CSS files.
- **Component Documentation**: Every component must have a `.stories.tsx` file for visualization in [Storybook](https://storybook.js.org/).
- **Naming Convention**: `PascalCase` for files and components (e.g., `TaskCard.tsx`).

## 3. The "Shadcn" Pattern
We utilize the `shadcn/ui` pattern:
1. **Copy/Paste Foundation**: Base UI components are initialized in the `ui` folder.
2. **Customization**: Components are then customized to match the Antigravity [Design Tokens](./DESIGN_TOKENS.md).

## 4. State Integration
- **Server State**: Use `TanStack Query` hooks (e.g., `useTask(id)`) inside Organisms.
- **Client State**: Use `Zustand` stores for cross-component UI state (e.g., `useTraceStore`).
- **Context**: Use React Context only for global configuration (Theming, Auth).

## 5. Performance Optimization
- **Re-render Control**: Use `React.memo` for high-frequency components in the Trace Stream.
- **Dynamic Imports**: Code-split large organisms (like the State Graph) using `next/dynamic`.
- **Skeleton States**: Every functional component must export a `Skeleton` variant for loading states.
