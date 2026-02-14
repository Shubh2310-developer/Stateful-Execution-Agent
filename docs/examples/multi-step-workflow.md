# Example: Multi-Step Workflow

This example illustrates a more complex, multi-step execution involving data processing and document generation.

## Scenario: Marketing Campaign Analysis

**Goal:** "Analyze the CSV file 'campaign_results.csv', calculate the ROI for each channel, and draft a summary report for the marketing director."

### Step 1: Goal Decomposition (Planner)
The agent parses the request and determines it needs:
1. A tool to read and process CSV data.
2. A tool to perform calculations.
3. A tool to generate a formatted document.

### Step 2: The Plan
1. `data_processor`: Load 'campaign_results.csv' and calculate ROI (ROI = (Revenue - Cost) / Cost).
2. `chart_generator`: Create a bar chart showing ROI by channel.
3. `summarizer`: Synthesize the raw data into key insights.
4. `document_generator`: Draft the final report including the charts and summary.
5. `pdf_generator`: Convert the report into a professional PDF.

### Step 3: Stateful Execution
- The agent executes Step 1 and stores the ROI data as a JSON artifact.
- It moves to Step 2, using the JSON artifact from Step 1 as input.
- If Step 3 fails validation (e.g., summary is too long), the agent pauses, saves its state, and allows the user to provide feedback.

### Step 4: Continuation
The user provides feedback: "Focus more on the Social Media ROI being lower than expected."
The agent replans Step 4 and 5 to incorporate this emphasis, then completes the task.
