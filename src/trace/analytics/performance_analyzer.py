from typing import List, Dict, Any
from datetime import datetime
from src.utils.logger import logger

class PerformanceAnalyzer:
    """Analyzes execution performance, latency, and token efficiency."""

    def analyze_latency(self, trace_entries: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculates latency metrics from trace entries."""
        if not trace_entries:
            return {}

        durations = [e.get("metadata", {}).get("duration_ms", 0) for e in trace_entries if "duration_ms" in e.get("metadata", {})]

        if not durations:
            return {"status": "no_duration_data"}

        return {
            "min_ms": min(durations),
            "max_ms": max(durations),
            "avg_ms": sum(durations) / len(durations),
            "p95_ms": sorted(durations)[int(len(durations) * 0.95)] if len(durations) > 0 else 0
        }

    def analyze_token_efficiency(self, trace_entries: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyzes token usage per successful outcome."""
        total_tokens = sum(e.get("metadata", {}).get("tokens_consumed", 0) for e in trace_entries)
        # This would compare tokens to task complexity or outcome quality
        return {"total_tokens": total_tokens, "efficiency_score": 1.0}
