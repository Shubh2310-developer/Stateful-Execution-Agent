import pytest
from datetime import datetime
from src.core.types import TaskState, Goal, TaskStatus, Step, Artifact

def test_task_state_validation():
    goal = Goal(request="Test goal", success_criteria=["Criteria 1"])
    state = TaskState(
        task_id="task-123",
        goal=goal,
        status=TaskStatus.PENDING
    )
    assert state.task_id == "task-123"
    assert state.status == TaskStatus.PENDING
    assert len(state.goal.success_criteria) == 1

def test_step_validation():
    step = Step(
        id="step-1",
        action="test",
        description="test description"
    )
    assert step.status == TaskStatus.PENDING

def test_artifact_validation():
    artifact = Artifact(
        id="art-1",
        uri="file:///tmp/test",
        type="data"
    )
    assert artifact.type == "data"
    assert isinstance(artifact.created_at, datetime)
