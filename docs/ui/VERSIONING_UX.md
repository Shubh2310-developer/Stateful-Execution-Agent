# Antigravity Versioning & Time Travel UX

The ability to "Time Travel" through an agent's state history is a core differentiator of Antigravity. This document defines the UI patterns for visualizing and interacting with versioned state.

## 1. The Version Timeline
A horizontal or vertical navigation component that allows users to move between state snapshots.

- **Visual Structure**: A series of nodes on a line, representing `version_id` updates.
- **Node Meta**:
  - **Timestamp**: When the version was created.
  - **Trigger**: What caused the update (e.g., "Step 2 Completed," "User Feedback Applied").
- **Current State Indicator**: A high-contrast marker showing which version the user is currently viewing.

## 2. The "Time Travel" View
When a user selects a historical version:

- **Read-only Badge**: A prominent "Viewing History (Read-only)" banner appears at the top.
- **State Restoration**: The Workplace and Trace panels update to show exactly what the agent knew and had produced at that moment.
- **Diff Highlighting**: Optionally highlight what changed between the *selected* version and the *previous* one.

## 3. Rollback Action
The primary functional use of time travel.

- **"Restore This Version" Button**: A primary CTA that appears when viewing a historical state.
- **Confirmation Modal**: A safety check explaining the impact: "Restoring this version will discard all subsequent steps and artifacts. This action is irreversible."
- **Trace Entry**: If a rollback occurs, it is logged in the Decision Trace: "User rolled back task to Version 12 (pre-analysis)."

## 4. Comparing Versions
- **Side-by-Side Mode**: Allow users to select two versions and see a split-screen comparison of the generated artifacts.
- **State Delta View**: A technical view showing the exact JSON diff between two state versions for debugging purposes.

## 5. Branching (Future Pattern)
- **Experimental Branches**: Allow a user to "Branch" from a historical version to test a different prompt or tool selection without affecting the "Main" execution path.
- **Branch Management**: A UI to switch between and eventually merge or discard experimental branches.
