"""Integration tests for Trace Visualization API endpoints."""

import pytest
from httpx import AsyncClient
from datetime import datetime
from src.api.app import app
from src.trace.trace_schema import DecisionTrace
from src.trace.decision_recorder import DecisionRecorder
from src.state.persistence.database_adapter import DatabaseAdapter


@pytest.mark.asyncio
class TestTraceVisualizationAPI:
    """Test the trace visualization API endpoints."""

    @pytest.fixture
    async def setup_test_data(self):
        """Set up test decision traces in the database."""
        # Create a database adapter and decision recorder
        db_adapter = DatabaseAdapter()
        recorder = DecisionRecorder(db_adapter=db_adapter)

        task_id = "test_viz_task_001"

        # Record several decisions
        await recorder.record_decision(
            task_id=task_id,
            step_id="step1",
            decision_point="Select Strategy",
            rationale="Strategy A has better performance",
            final_choice="Strategy A",
            options_considered=[
                {"name": "Strategy A", "score": 0.9},
                {"name": "Strategy B", "score": 0.6}
            ],
            confidence_score=0.9,
            risk_assessment="low",
            metadata={},
            tags=["planning"]
        )

        await recorder.record_decision(
            task_id=task_id,
            step_id="step1",
            decision_point="Execute Action",
            rationale="Using memory context from previous run",
            final_choice="Execute with Cache",
            options_considered=[
                {"name": "Execute Fresh"},
                {"name": "Execute with Cache"}
            ],
            confidence_score=0.7,
            risk_assessment="low",
            metadata={"memory_id": "mem_xyz_789"},
            tags=["execution"]
        )

        await recorder.record_decision(
            task_id=task_id,
            step_id="step2",
            decision_point="Error Recovery",
            rationale="Network timeout occurred",
            final_choice="Retry with Backoff",
            options_considered=[],
            confidence_score=0.4,
            risk_assessment="high",
            metadata={"error": "Network timeout after 30s"},
            tags=["error-recovery"]
        )

        yield task_id

        # Cleanup: delete test data
        await db_adapter.db.decisions.delete_many({"task_id": task_id})

    @pytest.mark.asyncio
    async def test_get_mermaid_visualization(self, setup_test_data):
        """Test GET /trace/task/{task_id}/visualization/mermaid endpoint."""
        task_id = await setup_test_data

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get(f"/trace/task/{task_id}/visualization/mermaid")

        assert response.status_code == 200
        mermaid_output = response.text

        # Verify Mermaid structure
        assert "graph TD" in mermaid_output
        assert "start([Start])" in mermaid_output
        assert "end_node([End])" in mermaid_output

        # Verify decision points appear
        assert "Select Strategy" in mermaid_output
        assert "Execute Action" in mermaid_output
        assert "Error Recovery" in mermaid_output

        # Verify color coding (styling)
        assert "fill:#d4edda" in mermaid_output  # High confidence (green)
        assert "fill:#fff3cd" in mermaid_output or "fill:#f8d7da" in mermaid_output  # Medium or low

        # Verify memory link
        assert "mem_xyz_789" in mermaid_output
        assert "-.->" in mermaid_output  # Dotted link for memory

        # Verify error styling
        assert "fill:#f5c6cb" in mermaid_output  # Error node color

    @pytest.mark.asyncio
    async def test_get_markdown_visualization(self, setup_test_data):
        """Test GET /trace/task/{task_id}/visualization/markdown endpoint."""
        task_id = await setup_test_data

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get(f"/trace/task/{task_id}/visualization/markdown")

        assert response.status_code == 200
        markdown_output = response.text

        # Verify Markdown structure
        assert "# Decision Trace Log" in markdown_output
        assert "## Step:" in markdown_output

        # Verify confidence icons
        assert "🟢" in markdown_output  # High confidence
        assert "🟡" in markdown_output or "🔴" in markdown_output  # Medium or low

        # Verify decision details
        assert "Select Strategy" in markdown_output
        assert "**Choice**: Strategy A" in markdown_output
        assert "**Confidence**:" in markdown_output
        assert "**Risk**:" in markdown_output

        # Verify memory context
        assert "**Memory Context**:" in markdown_output
        assert "mem_xyz_789" in markdown_output

        # Verify error details
        assert "**Error**: ❗" in markdown_output
        assert "Network timeout" in markdown_output

    @pytest.mark.asyncio
    async def test_visualization_not_found(self):
        """Test visualization endpoints return 404 for non-existent task."""
        non_existent_task_id = "task_does_not_exist_999"

        async with AsyncClient(app=app, base_url="http://test") as client:
            mermaid_response = await client.get(
                f"/trace/task/{non_existent_task_id}/visualization/mermaid"
            )
            markdown_response = await client.get(
                f"/trace/task/{non_existent_task_id}/visualization/markdown"
            )

        assert mermaid_response.status_code == 404
        assert "No decisions found" in mermaid_response.json()["detail"]

        assert markdown_response.status_code == 404
        assert "No decisions found" in markdown_response.json()["detail"]

    @pytest.mark.asyncio
    async def test_visualization_empty_task(self):
        """Test visualization for task with no decisions."""
        # Create a task with no decisions
        empty_task_id = "empty_task_123"

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get(f"/trace/task/{empty_task_id}/visualization/mermaid")

        # Should return 404 since no decisions exist
        assert response.status_code == 404
