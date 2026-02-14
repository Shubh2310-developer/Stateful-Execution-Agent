import pytest
from src.memory.short_term.task_context import TaskContext

def test_task_context_updates():
    context = TaskContext(task_id="t1")

    assert context.task_id == "t1"
    assert context.working_variables == {}

    context.update_variable("key", "value")
    assert context.working_variables["key"] == "value"

    context.add_note("This is a test note")
    assert len(context.temporary_notes) == 1
    assert context.temporary_notes[0] == "This is a test note"
