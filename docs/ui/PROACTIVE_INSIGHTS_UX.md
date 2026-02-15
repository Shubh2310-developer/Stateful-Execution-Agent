# Antigravity Proactive Insights UX

Antigravity isn't just reactive; it uses its long-term memory to suggest tasks and improvements proactively. This document defines the patterns for agent-led insights.

## 1. The "Proactive Rail"
- **Placement**: A subtle sidebar or bottom drawer on the Dashboard.
- **Content**: A list of "Recommended Actions" or "Observation Cards."
- **Interaction**: "Draft Plan" button to instantly convert an insight into a mission.

## 2. Types of Proactive Insights
- **Routine Automation**: "I've noticed you run this report every Monday. Should I draft the plan for next week?"
- **Memory-based Correction**: "You previously preferred a more technical tone for this client. Should I adjust your current draft?"
- **Knowledge Gaps**: "I see 5 new Slack messages about 'Project X' that aren't in my Knowledge Base. Should I index them?"
- **Opportunity Detection**: "Based on the metrics I just analyzed, revenue retention is dipping. Should I start a root-cause analysis?"

## 3. Insight Visual Styles
- **The "Lightbulb" Icon**: Consistent marker for agent-led suggestions.
- **Certainty Gauges**: "I am 85% sure this task will be helpful to you."
- **Dismissal Feedback**: If a user dismisses an insight, the agent asks "Why?" to refine its future proactive logic.

## 4. Ambient Intelligence
- **Subtle Toasts**: "I've noticed a pattern in your feedback..."
- **"While You Were Away" Insights**: (See [STATEFUL_SESSION_UX.md](./STATEFUL_SESSION_UX.md)) - Highlighting trends discovered while the user was offline.

## 5. Governance of Proactivity
- **Intrusiveness Slider**: A setting to control how often the agent suggests tasks (from "Silent/Reactive" to "Aggressive/Co-pilot").
- **Scope Restriction**: Prevent the agent from suggesting tasks in certain restricted domains or toolsets.
