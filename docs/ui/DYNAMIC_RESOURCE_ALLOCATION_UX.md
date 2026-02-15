# Antigravity Dynamic Resource Allocation UX

For large swarms, compute and GPU resources must be balanced. This document defines how the UI visualizes the shifting of "Agent Power."

## 1. Resource "Currents"
- **Energy Flow Visualization**: A background ambient animation (subtle moving particles) that reflects the "Flow" of compute resources between different active missions.
- **Density Heatmap**: A 2D or 3D view of the organizational "Compute Cluster," showing which agents are consuming the most power.

## 2. Priority Steering
- **Agent Throttle**: A slider or "Dial" for each active task to adjust its resource priority (from "Background/Efficient" to "Turbo/Immediate").
- **Cost vs. Speed Tradeoff**: As a user slides the throttle, a real-time tooltip shows the predicted change in cost and completion time.

## 3. Resource Contention UI
- **The "Bottleneck" Alert**: If the organization hits its LLM rate limit or compute cap, the UI flags "Congestion" and suggests which tasks to pause.
- **Resource Auction**: In decentralized environments, a UI for "Bidding" for extra compute for high-priority missions.

## 4. GPU/Model Visibility
- **Provider Load Gauges**: Real-time status of the Groq/Anthropic/Local server loads.
- **Model Efficiency Benchmarks**: Comparison of "Reasoning per Watt/Dollar" for the active agents.

## 5. Automated Balancing
- **"Auto-balancing" Toggle**: Allow the system to automatically down-rank low-priority tasks when a "Critical" mission starts.
- **Handoff for Efficiency**: Visualizing the agent "Moving" its state to a cheaper/faster server for a specific sub-task.
