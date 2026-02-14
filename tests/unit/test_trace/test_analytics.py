import pytest
from src.trace.analytics.aggregator import TraceAggregator
from src.trace.analytics.performance_analyzer import PerformanceAnalyzer
from src.trace.analytics.pattern_detector import PatternDetector

def test_performance_analyzer_latency():
    analyzer = PerformanceAnalyzer()
    trace_entries = [
        {"metadata": {"duration_ms": 100}},
        {"metadata": {"duration_ms": 200}},
        {"metadata": {"duration_ms": 300}}
    ]

    result = analyzer.analyze_latency(trace_entries)
    assert result["avg_ms"] == 200
    assert result["min_ms"] == 100
    assert result["max_ms"] == 300

@pytest.mark.asyncio
async def test_pattern_detector_failures():
    detector = PatternDetector()
    history = [
        {"event_type": "error", "metadata": {"error_message": "Timeout"}},
        {"event_type": "error", "metadata": {"error_message": "Timeout"}},
        {"event_type": "execution", "metadata": {}}
    ]

    patterns = await detector.detect_failure_patterns("t1", history)
    assert len(patterns) == 1
    assert patterns[0]["pattern"] == "Timeout"
    assert patterns[0]["occurrences"] == 2
