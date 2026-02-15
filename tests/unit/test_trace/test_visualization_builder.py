import pytest
from datetime import datetime, timedelta
from src.trace.trace_schema import DecisionTrace
from src.trace.query.visualization_builder import VisualizationBuilder

class TestVisualizationBuilder:

    @pytest.fixture
    def builder(self):
        return VisualizationBuilder()

    @pytest.fixture
    def sample_traces(self):
        base_time = datetime(2023, 1, 1, 10, 0, 0)
        return [
            DecisionTrace(
                decision_id="d1",
                task_id="t1",
                step_id="step1",
                timestamp=base_time,
                decision_point="Select Tool",
                options_considered=[{"name": "Tool A"}, {"name": "Tool B"}],
                decision_rationale="Tool A is better",
                confidence_score=0.9,
                risk_assessment="low",
                final_choice="Tool A",
                metadata={},
                tags=[]
            ),
            DecisionTrace(
                decision_id="d2",
                task_id="t1",
                step_id="step1",
                timestamp=base_time + timedelta(minutes=1),
                decision_point="Execute Action",
                options_considered=[{"name": "Run Fast"}, {"name": "Run Safe"}],
                decision_rationale="Need speed",
                confidence_score=0.6,
                risk_assessment="medium",
                final_choice="Run Fast",
                metadata={"memory_id": "mem_123"},
                tags=[]
            ),
            DecisionTrace(
                decision_id="d3",
                task_id="t1",
                step_id="step2",
                timestamp=base_time + timedelta(minutes=2),
                decision_point="Handle Error",
                options_considered=[],
                decision_rationale="Something went wrong",
                confidence_score=0.3,
                risk_assessment="high",
                final_choice="Retry",
                metadata={"error": "Connection failed"},
                tags=[]
            )
        ]

    def test_to_mermaid_structure(self, builder, sample_traces):
        mermaid_code = builder.to_mermaid(sample_traces)

        # Check basic structure
        assert "graph TD" in mermaid_code
        assert "start([Start])" in mermaid_code
        assert "end_node([End])" in mermaid_code

        # Check nodes existence
        assert "dec_0" in mermaid_code
        assert "dec_1" in mermaid_code
        assert "dec_2" in mermaid_code

        # Check labels
        assert "/Select Tool/" in mermaid_code
        assert "/Execute Action/" in mermaid_code
        assert "/Handle Error/" in mermaid_code

        # Check links
        assert "start --> dec_0" in mermaid_code
        assert "dec_0 -->|Tool A| dec_1" in mermaid_code
        assert "dec_1 -->|Run Fast| dec_2" in mermaid_code

        # Check memory link
        assert "mem_1" in mermaid_code
        assert "(@Memory: mem_123)" in mermaid_code
        assert "mem_1 -.-> dec_1" in mermaid_code

    def test_to_mermaid_styling(self, builder, sample_traces):
        mermaid_code = builder.to_mermaid(sample_traces)

        # High confidence (dec_0) -> Greenish fill (#d4edda)
        assert "style dec_0 fill:#d4edda" in mermaid_code

        # Medium confidence (dec_1) -> Yellowish fill (#fff3cd)
        assert "style dec_1 fill:#fff3cd" in mermaid_code

        # Error/High Risk (dec_2) -> Reddish fill or border
        # trace[2] has error in metadata, so it should have error styling
        assert "style dec_2 fill:#f5c6cb" in mermaid_code
        assert "stroke-width:4px" in mermaid_code

    def test_to_markdown_tree(self, builder, sample_traces):
        md_output = builder.to_markdown_tree(sample_traces)

        # Check headers
        assert "# Decision Trace Log" in md_output
        assert "## Step: `step1`" in md_output
        assert "## Step: `step2`" in md_output

        # Check content
        assert "### 🟢" in md_output # High confidence icon
        assert "Select Tool" in md_output
        assert "**Choice**: Tool A" in md_output

        assert "### 🟡" in md_output # Medium confidence icon
        assert "Execute Action" in md_output
        assert "**Memory Context**: `Linked to Memory ID: mem_123`" in md_output

        assert "### 🔴" in md_output # Low confidence icon
        assert "Handle Error" in md_output
        assert "**Error**: ❗ Connection failed" in md_output

    def test_empty_traces(self, builder):
        assert "graph TD" in builder.to_mermaid([])
        assert "_No traces recorded._" in builder.to_markdown_tree([])
