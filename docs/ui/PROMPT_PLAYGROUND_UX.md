# Antigravity Prompt Playground UX

The Prompt Playground is a specialized sandbox where developers and prompt engineers can iterate on agent instructions in a safe, isolated environment.

## 1. Split-Screen Layout
- **Left Panel (Editor)**: The [Prompt Editor](./PROMPT_EDITOR_UX.md) with full syntax highlighting.
- **Center Panel (Input/Goal)**: A text area to enter a test goal and any mock context (Memory/Artifacts).
- **Right Panel (Output)**: A real-time rendering of the agent's response, including the generated Plan and initial Decision Trace.

## 2. Rapid Iteration Cycle
- **"Run" Button**: A high-visibility primary action (`Cmd + Enter`).
- **Live Diff**: An optional toggle to see how the output changed compared to the *previous* run in the same session.
- **Variable Injector**: A sidebar that lists all available variables in the system prompt, allowing users to quickly click and insert them into the editor.

## 3. Mocking & Simulation
- **Memory Mocker**: A UI to "Simulate" learned preferences (e.g., "Mock: User prefers technical tone") to test how the agent adapts its reasoning.
- **Tool Mocker**: Define mock return values for specific tools (e.g., "Mock: `web_search` returns 0 results") to test the agent's error handling and alternative path planning.

## 4. Performance Metrics (Simulated)
- **Token Usage**: Real-time counter showing the cost of the current prompt + output.
- **Reasoning Density**: A metric showing the ratio of "Meaningful Decisions" to "Token Count," helping to identify "wordy" or inefficient prompts.
- **Confidence Gauge**: Visualization of the agent's confidence in its generated plan based on the current instructions.

## 5. Saving & Exporting
- **Commit to Library**: Save the prompt as a named template in the organizational library.
- **Deploy to Live**: A gated action that promotes the sandbox prompt to the production agent (requires Admin approval).
- **Share Link**: Generate a unique URL to share the current playground state (Prompt + Goal + Output) with a colleague for review.
