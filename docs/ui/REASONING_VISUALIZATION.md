# Antigravity Reasoning Visualization

Visualizing "Chain of Thought" (CoT) and autonomous reasoning is the most complex part of the Antigravity UI. This document defines how we render the agent's internal logic.

## 1. The Decision Trace (Stream)
The primary feed of atomic "Thought Units."
- **Atomic Unit**: Each decision is a "Card" in the trace stream.
- **Content**:
  - **The Point**: What was being decided?
  - **The Options**: What alternatives were weighed?
  - **The Rationale**: Why was the choice made?
  - **The Source**: Which memory or artifact influenced this?

## 2. Visualizing Uncertainty
- **Confidence Badge**: A numerical score (0-1.0) on every thought unit.
- **Uncertainty Tint**: Cards with low confidence (< 0.7) are tinted Amber.
- **Human Help CTA**: A button that appears only on low-confidence cards: "Is this correct?"

## 3. Logical Dependency Graph
For complex reasoning, a list isn't enough.
- **Thought Nodes**: A DAG showing how Decision A led to Decision B.
- **Branching**: Visualize "Counterfactuals" — what would have happened if the agent chose Option B instead of Option A.

## 4. Memory Influence Visualization
- **Insight Lines**: A visual link (connector line) between a reasoning block and the specific Fact Card in the Memory view that triggered it.
- **Preference Highlighting**: Bold text for words or rules that were derived directly from the user's learned preferences.

## 5. Artifact Transformation History
- **Lineage Map**: A visualization showing how a piece of raw data (e.g., a CSV file) was "reasoned upon" and transformed through multiple steps into a final insight.
- **Verification Overlay**: Next to a generated artifact, show small "Reasoning Tags" that, when clicked, jump the user back to the specific Decision Trace entry that justified that part of the artifact.
