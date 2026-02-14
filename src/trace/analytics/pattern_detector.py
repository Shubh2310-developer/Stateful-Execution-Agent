from typing import List, Dict, Any
from src.utils.logger import logger

class PatternDetector:
    """Detects recurring reasoning or failure patterns in decision traces."""

    async def detect_failure_patterns(self, task_id: str, history: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identifies common causes of failure in the trace history."""
        patterns = []
        errors = [e for e in history if e.get("event_type") == "error"]

        # Simple frequency analysis of error messages
        error_counts = {}
        for err in errors:
            msg = err.get("metadata", {}).get("error_message", "Unknown error")
            error_counts[msg] = error_counts.get(msg, 0) + 1

        for msg, count in error_counts.items():
            if count > 1:
                patterns.append({"pattern": msg, "occurrences": count, "type": "repeated_error"})

        return patterns

    async def detect_successful_tool_chains(self, user_id: str, history: List[Dict[str, Any]]) -> List[List[str]]:
        """Identifies sequences of tools that often lead to successful outcomes."""
        return []
