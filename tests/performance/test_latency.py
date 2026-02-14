import pytest
import time
from src.llm.groq_client import groq_client
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_api_latency_simulation():
    """Simulates measuring latency for a Groq API call."""
    start_time = time.perf_counter()

    with patch("src.llm.groq_client.groq_client.generate_response") as mock_gen:
        mock_gen.return_value = "Test response"
        await groq_client.generate_response([{"role": "user", "content": "hello"}])

    end_time = time.perf_counter()
    latency = end_time - start_time
    assert latency < 1.0  # Should be very fast with mock
