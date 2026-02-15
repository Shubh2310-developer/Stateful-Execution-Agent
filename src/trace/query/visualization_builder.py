from typing import List, Dict, Any, Optional
from src.trace.trace_schema import DecisionTrace
from datetime import datetime

class VisualizationBuilder:
    """
    Converts decision traces into visual representations (Mermaid.js, Markdown).
    Helps in debugging and understanding agent behavior.
    """

    def to_mermaid(self, traces: List[DecisionTrace]) -> str:
        """
        Generates a Mermaid.js flowchart string from a list of decision traces.
        """
        if not traces:
            return "graph TD\n    start[Start] --> end_node[End]"

        mermaid_lines = ["graph TD"]

        # Sort traces by timestamp to ensure correct flow
        sorted_traces = sorted(traces, key=lambda x: x.timestamp)

        # Start node
        mermaid_lines.append("    start([Start])")

        previous_node_id = "start"

        for i, trace in enumerate(sorted_traces):
            node_id = f"dec_{i}"

            # Sanitize label for mermaid (remove quotes, parens)
            safe_label = trace.decision_point.replace('"', "'").replace('(', '').replace(')', '')
            if len(safe_label) > 40:
                safe_label = safe_label[:37] + "..."

            safe_choice = trace.final_choice.replace('"', "'")
            if len(safe_choice) > 30:
                safe_choice = safe_choice[:27] + "..."

            # Create node definition
            # Shape: /Decision/ for decisions
            node_def = f"    {node_id}[/{safe_label}/]"
            mermaid_lines.append(node_def)

            # Style the node
            style_def = self._get_mermaid_style(node_id, trace)
            if style_def:
                mermaid_lines.append(style_def)

            # Link from previous
            if i == 0:
                mermaid_lines.append(f"    {previous_node_id} --> {node_id}")
            else:
                # Use the previous choice as the edge label if available
                prev_trace = sorted_traces[i-1]
                prev_choice = prev_trace.final_choice.replace('"', "'")
                if len(prev_choice) > 20:
                    prev_choice = prev_choice[:17] + "..."
                mermaid_lines.append(f"    {previous_node_id} -->|{prev_choice}| {node_id}")

            # Add memory link if present
            if trace.metadata and "memory_id" in trace.metadata:
                mem_id = trace.metadata["memory_id"]
                mem_node_id = f"mem_{i}"
                mermaid_lines.append(f"    {mem_node_id}[(@Memory: {mem_id})]")
                mermaid_lines.append(f"    {mem_node_id} -.-> {node_id}")
                mermaid_lines.append(f"    style {mem_node_id} fill:#e1f5fe,stroke:#0277bd")

            # Update previous node
            previous_node_id = node_id

        # End node
        last_trace = sorted_traces[-1]
        last_choice = last_trace.final_choice.replace('"', "'")
        if len(last_choice) > 20:
            last_choice = last_choice[:17] + "..."

        mermaid_lines.append(f"    {previous_node_id} -->|{last_choice}| end_node([End])")

        return "\n".join(mermaid_lines)

    def _get_mermaid_style(self, node_id: str, trace: DecisionTrace) -> str:
        """
        Returns Mermaid style string based on confidence and risk.
        """
        # Determine color based on confidence
        if trace.confidence_score >= 0.8:
            fill = "#d4edda" # Greenish (High confidence)
            stroke = "#28a745"
        elif trace.confidence_score >= 0.5:
            fill = "#fff3cd" # Yellowish (Medium confidence)
            stroke = "#ffc107"
        else:
            fill = "#f8d7da" # Reddish (Low confidence)
            stroke = "#dc3545"

        # Check for error in metadata
        if trace.metadata and (trace.metadata.get("error") or trace.metadata.get("status") == "failed"):
            fill = "#f5c6cb"
            stroke = "#721c24"
            stroke_width = "4px"
        elif trace.risk_assessment == "high":
            stroke_width = "4px"
            stroke = "#dc3545" # Red border for high risk
        else:
            stroke_width = "2px"

        return f"    style {node_id} fill:{fill},stroke:{stroke},stroke-width:{stroke_width}"

    def to_markdown_tree(self, traces: List[DecisionTrace]) -> str:
        """
        Generates a Markdown representation of the decision trace.
        """
        if not traces:
            return "_No traces recorded._"

        sorted_traces = sorted(traces, key=lambda x: x.timestamp)
        md_lines = ["# Decision Trace Log", ""]

        current_step_id = None

        for trace in sorted_traces:
            # Group by Step ID if it changes
            if trace.step_id and trace.step_id != current_step_id:
                md_lines.append(f"## Step: `{trace.step_id}`")
                current_step_id = trace.step_id
            elif current_step_id is None and trace.step_id:
                 md_lines.append(f"## Step: `{trace.step_id}`")
                 current_step_id = trace.step_id

            timestamp_str = trace.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            icon = self._get_confidence_icon(trace.confidence_score)

            # Title line
            md_lines.append(f"### {icon} [{timestamp_str}] {trace.decision_point}")

            # Details block
            md_lines.append(f"- **ID**: `{trace.decision_id}`")
            md_lines.append(f"- **Choice**: {trace.final_choice}")
            md_lines.append(f"- **Rationale**: {trace.decision_rationale}")
            md_lines.append(f"- **Confidence**: {trace.confidence_score:.2f}")
            md_lines.append(f"- **Risk**: {trace.risk_assessment}")

            if trace.options_considered:
                md_lines.append("- **Options Considered**:")
                for opt in trace.options_considered:
                    label = str(opt)
                    if isinstance(opt, dict):
                        label = opt.get('name') or opt.get('id') or label
                    # Truncate if too long
                    if len(label) > 100:
                        label = label[:97] + "..."
                    md_lines.append(f"  - {label}")

            if trace.metadata:
                # Check for memory usage
                if 'memory_id' in trace.metadata:
                     md_lines.append(f"- **Memory Context**: `Linked to Memory ID: {trace.metadata['memory_id']}`")

                # Check for errors
                if 'error' in trace.metadata:
                     md_lines.append(f"- **Error**: ❗ {trace.metadata['error']}")

            md_lines.append("") # Empty line between entries

        return "\n".join(md_lines)

    def _get_confidence_icon(self, score: float) -> str:
        if score >= 0.8:
            return "🟢" # High
        elif score >= 0.5:
            return "🟡" # Medium
        else:
            return "🔴" # Low
