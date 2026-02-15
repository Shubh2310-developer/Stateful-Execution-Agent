import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock
from src.trace.context import set_trace_context, get_current_context, get_task_id, get_step_id
from src.trace.decorators import traced_decision

@pytest.mark.asyncio
async def test_context_propagation():
    """Test that context is correctly set and retrieved."""
    task_id = "task_123"
    step_id = "step_456"

    # Set context
    set_trace_context(task_id=task_id, step_id=step_id, metadata={"test": True})

    # Verify context retrieval
    ctx = get_current_context()
    assert ctx.task_id == task_id
    assert ctx.step_id == step_id
    assert ctx.metadata == {"test": True}

    assert get_task_id() == task_id
    assert get_step_id() == step_id

@pytest.mark.asyncio
async def test_context_isolation():
    """Test that context is isolated between tasks."""

    async def task_a():
        set_trace_context(task_id="task_A")
        await asyncio.sleep(0.01)
        return get_task_id()

    async def task_b():
        set_trace_context(task_id="task_B")
        await asyncio.sleep(0.01)
        return get_task_id()

    # Run concurrently
    results = await asyncio.gather(task_a(), task_b())

    assert results[0] == "task_A"
    assert results[1] == "task_B"

@pytest.mark.asyncio
async def test_traced_decision_decorator():
    """Test the @traced_decision decorator logs events."""

    # Mock the trace_logger used in decorators
    with patch('src.trace.decorators.trace_logger') as mock_logger:
        mock_logger.log_event = AsyncMock()

        # Define a decorated function
        @traced_decision(event_type="test_exec")
        async def sample_function(x, y):
            return x + y

        # Call the function
        result = await sample_function(5, 10)

        # Verify result
        assert result == 15

        # Verify logger was called
        # Note: logging happens in background task, so we might need to yield to event loop
        # But since we mock log_event returning a coroutine, and we don't await the task in the test,
        # we need to make sure the task is actually scheduled.
        # The decorator uses asyncio.create_task(trace_logger.log_event(...))

        # Give the event loop a moment to process the background task
        await asyncio.sleep(0.01)

        assert mock_logger.log_event.called

        call_args = mock_logger.log_event.call_args
        assert call_args is not None
        kwargs = call_args.kwargs

        assert kwargs['event_type'] == "test_exec"
        assert kwargs['context']['inputs'] == {'x': '5', 'y': '10'}
        assert kwargs['outcome']['result'] == '15'
        assert kwargs['outcome']['status'] == 'success'

@pytest.mark.asyncio
async def test_traced_decision_error_handling():
    """Test the @traced_decision decorator handles and logs errors."""

    with patch('src.trace.decorators.trace_logger') as mock_logger:
        mock_logger.log_event = AsyncMock()

        @traced_decision(event_type="test_error")
        async def failing_function():
            raise ValueError("Something went wrong")

        # Verify exception is raised
        with pytest.raises(ValueError):
            await failing_function()

        # Give the event loop a moment
        await asyncio.sleep(0.01)

        # Verify error logging
        assert mock_logger.log_event.called
        kwargs = mock_logger.log_event.call_args.kwargs

        assert kwargs['outcome']['status'] == 'error'
        assert 'Something went wrong' in kwargs['outcome']['error']
