import pytest
from src.memory.long_term.user_profile import UserProfile, UserPreferences
from src.memory.long_term.historical_analyzer import HistoricalAnalyzer
from src.memory.long_term.pattern_learner import PatternLearner

def test_user_profile_creation():
    profile = UserProfile(user_id="u1", role="Dev", company="ACME")
    assert profile.user_id == "u1"
    assert profile.communication_style == "professional"

def test_user_preferences_update():
    prefs = UserPreferences()
    prefs.update_preference("document_tone", "casual")
    prefs.update_preference("custom_key", "custom_value")

    assert prefs.document_tone == "casual"
    assert prefs.formatting_rules["custom_key"] == "custom_value"

def test_historical_analyzer():
    analyzer = HistoricalAnalyzer()
    history = [
        {"success_score": 0.9},
        {"success_score": 0.4},
        {"success_score": 0.95}
    ]
    result = analyzer.analyze_trends(history)
    assert result["total_tasks"] == 3
    assert result["success_rate"] == pytest.approx(0.666, 0.01)

def test_pattern_learner():
    learner = PatternLearner()
    patterns = []
    new_exp = {"task_type": "test", "approach": "none"}

    updated = learner.update_patterns(patterns, new_exp)
    assert len(updated) == 1
    assert updated[0] == new_exp
