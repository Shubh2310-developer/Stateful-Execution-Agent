# Antigravity UI Error & Empty States

In an autonomous agentic system, how failures and lack of data are handled is as important as the successful execution flow. This document defines the patterns for Error and Empty states in the Antigravity UI.

## 1. Empty States

Empty states should be used to guide the user, not just indicate a lack of data.

- **Initial State (No Tasks)**: When a user first opens the dashboard, display a "Welcome" hero section with a primary CTA to "Create New Task" and quick-start templates.
- **No Search Results**: If a search in the task history returns nothing, show a "No Matches Found" message with suggestions to broaden the search criteria.
- **Empty Memory**: If the agent hasn't learned any preferences yet, show a "Starting Fresh" card explaining how the agent learns over time.
- **Visuals**: Use muted SVG illustrations or Lucide icons (e.g., `Inbox` or `Search` icons) at `w-12 h-12` or larger, centered with a `text-slate-400` color.

## 2. Error Categorization & Handling

Errors are categorized by their severity and the required user action.

### 2.1 Transient Errors (Auto-Recoverable)
Errors like API timeouts or temporary network glitches.
- **UI Pattern**: Inline status message in the Trace Panel.
- **Visual**: Amber text (`text-amber-500`) with a "Retrying..." spinner or countdown.
- **User Action**: None required, but visibility is maintained for transparency.

### 2.2 Validation Failures (Non-Critical)
The agent produced an output that didn't meet success criteria but is still functioning.
- **UI Pattern**: Highlighted card in the Trace Panel with a "Needs Review" badge.
- **Visual**: Amber border (`border-amber-300`) and a specialized action button ("Fix" or "Accept Anyway").
- **User Action**: Manual approval or adjustment of the step's parameters.

### 2.3 Critical Blockers (Action Required)
Authentication failures, missing tools, or contradictory user goals.
- **UI Pattern**: Modal overlay or high-visibility red banner at the top of the Workplace.
- **Visual**: Red background/text (`bg-red-50 text-red-700`) with a clear error code and description.
- **User Action**: Must resolve the issue (e.g., update API key, clarify goal) before execution can continue.

### 2.4 System Crashes (Fatal)
The backend or API is unreachable.
- **UI Pattern**: Full-screen "System Offline" state.
- **Visual**: Large error icon, technical details hidden behind a "Details" toggle, and a "Retry Connection" button.

## 3. The "Undo" & "Rollback" Pattern

Since the agent is stateful, errors can often be "fixed" by going back in time.

- **Checkpoint Restoration**: When an error occurs, the UI should offer a "Rollback to [Last Successful Step]" button.
- **Correction Loop**: Allow users to edit the "Failed Step" inputs directly from the error message and hit "Retry with New Parameters."

## 4. Copywriting for Errors

- **Be Clear, Not Technical**: Instead of "504 Gateway Timeout," use "The Metrics API is taking too long to respond. We are retrying now."
- **Provide Next Steps**: Always tell the user what they can do to fix the problem.
- **Maintain Calm**: Use professional, non-alarmist language.
