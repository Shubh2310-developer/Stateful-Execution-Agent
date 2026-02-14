from typing import List, Dict, Any
from src.core.types import TaskState
from src.utils.logger import logger

class PatternExtractor:
    """Analyzes task history to extract reusable strategies and patterns."""

    def extract_patterns(self, state: TaskState) -> List[Dict[str, Any]]:
        """Identifies what made the task successful or where it struggled."""
        patterns = []

        if state.status == "completed":
            # Extract sequence of successful tool uses
            tool_sequence = [d.choice_made for d in state.decisions]
            patterns.append({
                "type": "successful_strategy",
                "goal_type": state.goal.request,
                "tools": tool_sequence,
                "confidence_avg": sum(d.confidence for d in state.decisions) / len(state.decisions) if state.decisions else 0
            })

        return patterns
