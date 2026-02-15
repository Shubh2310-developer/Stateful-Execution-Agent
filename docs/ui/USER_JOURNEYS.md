# Antigravity User Journeys

This document outlines the core workflows for operators using the Antigravity UI to manage autonomous agentic tasks.

## 1. Journey: Goal Initiation & Planning

**Goal**: The user wants the agent to perform a complex, multi-step task.

1. **Initiation**: User types a high-level goal into the "New Task" input (e.g., "Analyze the last 3 months of customer feedback and suggest 5 product improvements").
2. **Context Enrichment**: The UI shows a subtle "Gathering Context" indicator while the agent retrieves user preferences and relevant memory.
3. **Plan Preview**: The agent presents a 5-8 step plan.
4. **Refinement**: The user reviews the plan and adds a constraint: "Make sure to exclude feedback from the beta group."
5. **Approval**: User clicks "Execute Plan." The view transitions to **Mission Control**.

## 2. Journey: Active Monitoring (The "Glass Box")

**Goal**: The user wants to ensure the agent is making correct decisions during a long-running task.

1. **Dashboard Overview**: User sees the active task card with a pulsing "Running" status and a progress bar at 40%.
2. **Trace Deep Dive**: User clicks "View Trace." The right panel opens, showing the stream of decisions.
3. **Reasoning Audit**: User reads a specific decision: "Selected 'Positive Sentiment' filter based on previous preference for growth-oriented reports."
4. **Validation**: User sees a success checkmark next to "Step 2: Filter raw data."
5. **Real-time Artifact**: User watches as the "Product Improvements Draft" Markdown file begins to stream content in the center Workplace area.

## 3. Journey: Intervention & Correction

**Goal**: The agent is heading down an incorrect path, and the user needs to correct it.

1. **Checkpoint Alert**: The agent hits a low-confidence decision point and pauses. The UI pulses Amber and shows a "Decision Required" notification.
2. **Context Review**: User opens the Trace entry to see the agent's confusion: "Two conflicting data sources found for 'Churn Rate'. Source A says 5%, Source B says 12%."
3. **Human Correction**: User types into the feedback box: "Source B is the more recent internal dashboard, use that."
4. **Resumption**: User clicks "Continue with Feedback." The agent logs the correction in the Trace and resumes Step 3.

## 4. Journey: Final Review & Artifact Export

**Goal**: The task is complete, and the user needs to finalize the output.

1. **Completion Notification**: User receives a toast: "Task Complete: Product Improvement Recommendations Ready."
2. **Quality Audit**: User reviews the final document in the Workplace. They check the automatically generated "Success Criteria" list to see if all goals were met.
3. **Refinement Loop**: User clicks "Refine" and asks the agent to "Add a section on feasibility for each improvement."
4. **Export**: Once satisfied, the user clicks "Export to PDF."
5. **Memory Update**: The user gives a 5-star rating. The UI shows: "Learning saved: You prefer feasibility analysis in strategy reports."

## 5. Journey: Historical Audit & Learning

**Goal**: The user wants to see how a similar task was handled 2 months ago.

1. **Task Query**: User searches "product improvements" in the Task History.
2. **Historical View**: User opens `task_047`. The UI loads the full trace and state as it existed then.
3. **Pattern Inspection**: User sees that for `task_047`, the agent correctly identified "UX friction" as a key theme.
4. **Comparison**: User compares the current task's performance with the historical one using the Analytics view.
