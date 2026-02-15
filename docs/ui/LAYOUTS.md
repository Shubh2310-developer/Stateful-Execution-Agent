# Antigravity UI Layouts

This document defines the primary page structures for the Antigravity application.

## 1. Global Structure
The application follows a standard high-productivity dashboard layout:
- **Sidebar (Fixed Left)**: Navigation (Dashboard, Tasks, Memory, Settings).
- **Header (Fixed Top)**: Search, Notifications, User Profile, Current Task Status.
- **Main Content (Scrollable)**: The primary working area.
- **Trace Panel (Fixed/Collapsible Right)**: Real-time decision log and agent "thinking" process.

## 2. Main Dashboard (Overview)
The landing view for the operator.
- **Hero Stats**:
  - Active Tasks (running now).
  - Memory Health (learned patterns count).
  - Efficiency Score (time saved vs manual).
- **Active Task Grid**: 2 or 3 columns of `TaskCard` components showing ongoing work.
- **Recent Artifacts**: A table or list of the latest documents/data generated.

## 3. Task Execution View (The "Mission Control")
The primary view for a specific task.
- **Left Column (Plan)**: A vertical `StepIndicator` list showing completed, current, and pending steps.
- **Center Area (Workplace)**:
  - **Live Preview**: Real-time rendering of the artifact being generated (Markdown/Table/Chart).
  - **Resource Manager**: List of inputs (Files, APIs) being used for the current step.
- **Right Column (Trace)**: The `DecisionTraceEntry` stream. This scrolls automatically as the agent works.

## 4. Trace & Analytics View
A deep-dive view for debugging or auditing agent behavior.
- **Decision Chain**: A visual graph (DAG) of the decision tree for the task.
- **Detail Panel**: Full JSON/Markdown view of specific trace entries, including prompt context and LLM raw outputs.
- **Resource Usage**: Charts showing token consumption and API latency over the task lifecycle.

## 5. Memory Management View
- **Preference Cards**: Editable cards for learned user preferences.
- **Domain Graph**: A visualization of the "concepts" and "patterns" the agent has learned about the user's business.
- **Pattern Library**: List of historical tasks used as exemplars for future planning.
