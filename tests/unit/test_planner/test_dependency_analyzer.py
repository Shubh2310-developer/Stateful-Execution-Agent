import pytest
from src.planner.dependency_analyzer import DependencyAnalyzer
from src.core.types import Step
from src.core.exceptions import ValidationError

def test_topological_sort_success():
    analyzer = DependencyAnalyzer()
    steps = [
        Step(step_id="S1", action="A1", description="D1", dependencies=[]),
        Step(step_id="S2", action="A2", description="D2", dependencies=["S1"]),
        Step(step_id="S3", action="A3", description="D3", dependencies=["S1", "S2"]),
    ]

    sorted_steps = analyzer.analyze(steps)

    assert len(sorted_steps) == 3
    assert sorted_steps[0].step_id == "S1"
    assert sorted_steps[1].step_id == "S2"
    assert sorted_steps[2].step_id == "S3"

    # Check order assignment
    assert sorted_steps[0].order == 1
    assert sorted_steps[1].order == 2
    assert sorted_steps[2].order == 3

def test_circular_dependency():
    analyzer = DependencyAnalyzer()
    steps = [
        Step(step_id="S1", action="A1", description="D1", dependencies=["S2"]),
        Step(step_id="S2", action="A2", description="D2", dependencies=["S1"]),
    ]

    with pytest.raises(ValidationError) as excinfo:
        analyzer.analyze(steps)
    assert "Circular dependency detected" in str(excinfo.value)

def test_missing_dependency():
    analyzer = DependencyAnalyzer()
    steps = [
        Step(step_id="S1", action="A1", description="D1", dependencies=["S99"]),
    ]

    with pytest.raises(ValidationError) as excinfo:
        analyzer.analyze(steps)
    assert "depends on non-existent step: S99" in str(excinfo.value)

def test_get_executable_steps():
    analyzer = DependencyAnalyzer()
    steps = [
        Step(step_id="S1", action="A1", description="D1", dependencies=[]),
        Step(step_id="S2", action="A2", description="D2", dependencies=["S1"]),
        Step(step_id="S3", action="A3", description="D3", dependencies=[]),
    ]

    # Initially S1 and S3 should be executable
    executable = analyzer.get_executable_steps(steps, [])
    assert len(executable) == 2
    ids = [s.step_id for s in executable]
    assert "S1" in ids
    assert "S3" in ids
    assert "S2" not in ids

    # After S1 is completed, S2 should become executable
    executable_after_s1 = analyzer.get_executable_steps(steps, ["S1"])
    assert len(executable_after_s1) == 2
    ids_after_s1 = [s.step_id for s in executable_after_s1]
    assert "S2" in ids_after_s1
    assert "S3" in ids_after_s1
