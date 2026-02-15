from fastapi import APIRouter, HTTPException, Request, Query
from fastapi.responses import PlainTextResponse
from src.trace.query.trace_query_engine import TraceQueryEngine
from src.trace.query.visualization_builder import VisualizationBuilder
from src.trace.trace_schema import TraceEntry, DecisionTrace
from typing import List, Optional

router = APIRouter(prefix="/trace", tags=["trace"])
query_engine = TraceQueryEngine()
viz_builder = VisualizationBuilder()

@router.get("/task/{task_id}", response_model=List[TraceEntry])
async def get_task_traces(
    task_id: str,
    event_type: Optional[str] = None,
    limit: int = 100
):
    """Retrieves the execution trace for a specific task."""
    traces = await query_engine.query_traces(task_id=task_id, event_type=event_type, limit=limit)
    return traces

@router.get("/task/{task_id}/decisions", response_model=List[DecisionTrace])
async def get_task_decisions(task_id: str):
    """Retrieves all major decisions made for a specific task."""
    decisions = await query_engine.get_decisions_by_task(task_id)
    return decisions

@router.get("/task/{task_id}/step/{step_id}", response_model=List[TraceEntry])
async def get_step_traces(task_id: str, step_id: str):
    """Retrieves traces for a specific step within a task."""
    return await query_engine.get_step_trace(task_id, step_id)

@router.get("/search/low-confidence", response_model=List[DecisionTrace])
async def get_low_confidence_decisions(
    threshold: float = Query(0.5, ge=0.0, le=1.0),
    limit: int = 50
):
    """Finds decisions where the agent had low confidence (< threshold)."""
    return await query_engine.get_low_confidence_decisions(threshold, limit)

@router.get("/search/reasoning", response_model=List[DecisionTrace])
async def search_reasoning(
    keyword: str,
    limit: int = 50
):
    """Full-text search through decision rationales."""
    return await query_engine.search_reasoning(keyword, limit)

@router.get("/task/{task_id}/visualization/mermaid", response_class=PlainTextResponse)
async def get_task_visualization_mermaid(task_id: str):
    """
    Generates a Mermaid.js flowchart visualization of the decision trace for a task.

    Visual Cues:
    - Green nodes: High confidence (>= 0.8)
    - Yellow nodes: Medium confidence (0.5 - 0.8)
    - Red nodes: Low confidence (< 0.5)
    - Thick borders: Errors or high-risk decisions
    - Dotted links: Memory references
    """
    decisions = await query_engine.get_decisions_by_task(task_id)
    mermaid_code = viz_builder.to_mermaid(decisions)
    return mermaid_code

@router.get("/task/{task_id}/visualization/markdown", response_class=PlainTextResponse)
async def get_task_visualization_markdown(task_id: str):
    """
    Generates a Markdown tree visualization of the decision trace for a task.

    Includes:
    - Decision IDs and timestamps
    - Choices made and rationale
    - Confidence scores with visual indicators (🟢🟡🔴)
    - Memory context links
    - Error details
    """
    decisions = await query_engine.get_decisions_by_task(task_id)
    if not decisions:
        raise HTTPException(status_code=404, detail=f"No decisions found for task {task_id}")

    markdown_output = viz_builder.to_markdown_tree(decisions)
    return markdown_output

