"""
Example: Using the Enhanced Reviewer Module

This example demonstrates how to use the Reviewer with self-correction loop
to evaluate task execution quality and request revisions when needed.
"""

import asyncio
from datetime import datetime
from src.reviewer.reviewer import Reviewer
from src.reviewer.quality_checker import QualityChecker
from src.core.types import (
    TaskState, Goal, Plan, Step, Artifact, TaskStatus
)


async def example_successful_review():
    """Example of a task that passes review on first attempt."""
    print("=" * 80)
    print("EXAMPLE 1: Successful Review (First Attempt)")
    print("=" * 80)

    # Create a well-executed task
    goal = Goal(
        request="Create a Python script to analyze sales data",
        success_criteria=[
            "Script must read CSV file",
            "Calculate total sales and averages",
            "Generate summary report",
            "Include error handling"
        ],
        constraints=["Use pandas library", "Professional code style"]
    )

    step = Step(
        step_id="step_001",
        order=1,
        action="generate_code",
        description="Generate Python sales analysis script",
        success_criteria="Complete, runnable script with all requirements",
        status=TaskStatus.COMPLETED
    )

    plan = Plan(task_id="task_001", steps=[step])

    # Simulated artifact (in real usage, this would be actual code)
    artifact = Artifact(
        id="art_001",
        task_id="task_001",
        step_id="step_001",
        uri="file:///tmp/sales_analysis.py",
        type="code",
        mime_type="text/x-python",
        size_bytes=2500
    )

    state = TaskState(
        task_id="task_001",
        user_id="user_123",
        goal=goal,
        plan=plan,
        artifacts=[artifact],
        status=TaskStatus.COMPLETED,
        current_step_index=1
    )

    # Initialize reviewer
    reviewer = Reviewer(max_iterations=2)

    # Run review (in production, you'd use review_with_correction_loop)
    print("\nRunning review...")
    # Note: This would fail in practice without proper mocking/setup
    # result = await reviewer.review_task(state)

    # Simulated result for demonstration
    result = {
        "task_id": "task_001",
        "overall_success": True,
        "needs_revision": False,
        "quality_score": 87.5,
        "quality_breakdown": {
            "llm_review_score": 85,
            "artifact_quality_scores": {"art_001": 92.0}
        },
        "requirement_coverage": {
            "total_requirements": 4,
            "met_requirements": 4,
            "coverage_percentage": 100
        },
        "strengths": [
            "Clean, well-structured code",
            "Comprehensive error handling",
            "Good documentation"
        ],
        "weaknesses": [],
        "revision_instructions": [],
        "feedback": "Excellent implementation. All requirements met with high quality.",
        "iteration_count": 0
    }

    print("\n" + "=" * 40)
    print("REVIEW RESULTS")
    print("=" * 40)
    print(f"Overall Success: {result['overall_success']}")
    print(f"Quality Score: {result['quality_score']}/100")
    print(f"Needs Revision: {result['needs_revision']}")
    print(f"Iteration: {result['iteration_count']}")
    print(f"\nRequirement Coverage: {result['requirement_coverage']['coverage_percentage']}%")
    print(f"\nStrengths:")
    for strength in result['strengths']:
        print(f"  ✓ {strength}")
    print(f"\nFeedback: {result['feedback']}")


async def example_revision_needed():
    """Example of a task that needs revision."""
    print("\n\n")
    print("=" * 80)
    print("EXAMPLE 2: Review Requiring Revision")
    print("=" * 80)

    # Create a task with quality issues
    goal = Goal(
        request="Write a technical blog post about microservices",
        success_criteria=[
            "Must include introduction, body, and conclusion",
            "Cover at least 3 key microservice patterns",
            "Include code examples",
            "Professional, engaging tone"
        ],
        constraints=["1000-1500 words", "Technical but accessible"]
    )

    step = Step(
        step_id="step_001",
        order=1,
        action="generate_document",
        description="Write blog post on microservices",
        success_criteria="Complete blog post meeting all criteria",
        status=TaskStatus.COMPLETED
    )

    plan = Plan(task_id="task_002", steps=[step])

    artifact = Artifact(
        id="art_002",
        task_id="task_002",
        step_id="step_001",
        uri="file:///tmp/blog_post.md",
        type="document",
        mime_type="text/markdown",
        size_bytes=800  # Too short!
    )

    state = TaskState(
        task_id="task_002",
        user_id="user_123",
        goal=goal,
        plan=plan,
        artifacts=[artifact],
        status=TaskStatus.COMPLETED,
        current_step_index=1
    )

    # Simulated review result showing revision needed
    result = {
        "task_id": "task_002",
        "overall_success": False,
        "needs_revision": True,
        "quality_score": 62.0,
        "quality_breakdown": {
            "llm_review_score": 60,
            "artifact_quality_scores": {"art_002": 65.0}
        },
        "requirement_coverage": {
            "total_requirements": 4,
            "met_requirements": 2,
            "partially_met": 1,
            "unmet_requirements": 1,
            "coverage_percentage": 50
        },
        "success_criteria_status": [
            {
                "criterion": "Must include introduction, body, and conclusion",
                "status": "MET",
                "evidence": "All three sections present"
            },
            {
                "criterion": "Cover at least 3 key microservice patterns",
                "status": "PARTIALLY_MET",
                "evidence": "Only 2 patterns covered (API Gateway, Service Discovery)"
            },
            {
                "criterion": "Include code examples",
                "status": "NOT_MET",
                "evidence": "No code examples found in document"
            },
            {
                "criterion": "Professional, engaging tone",
                "status": "MET",
                "evidence": "Tone is appropriate"
            }
        ],
        "strengths": [
            "Good structure with clear sections",
            "Professional writing style"
        ],
        "weaknesses": [
            "Document is only 800 words (requirement: 1000-1500)",
            "Missing third microservice pattern",
            "No code examples provided",
            "Conclusion section is too brief"
        ],
        "revision_instructions": [
            "Add a third microservice pattern (e.g., Circuit Breaker, Event Sourcing, or CQRS)",
            "Include at least 2 code examples demonstrating key concepts",
            "Expand the document to at least 1000 words by adding more detail to each pattern",
            "Strengthen the conclusion with specific takeaways and recommendations"
        ],
        "feedback": "The blog post has good structure and tone, but falls short on technical depth and completeness. Needs additional content to meet word count and coverage requirements.",
        "iteration_count": 0
    }

    print("\n" + "=" * 40)
    print("REVIEW RESULTS")
    print("=" * 40)
    print(f"Overall Success: {result['overall_success']}")
    print(f"Quality Score: {result['quality_score']}/100")
    print(f"Needs Revision: {result['needs_revision']}")
    print(f"Iteration: {result['iteration_count']}")

    print(f"\nRequirement Coverage: {result['requirement_coverage']['coverage_percentage']}%")
    print(f"  ✓ Met: {result['requirement_coverage']['met_requirements']}")
    print(f"  ~ Partially Met: {result['requirement_coverage']['partially_met']}")
    print(f"  ✗ Unmet: {result['requirement_coverage']['unmet_requirements']}")

    print(f"\nSuccess Criteria Status:")
    for criterion in result['success_criteria_status']:
        status_symbol = {"MET": "✓", "PARTIALLY_MET": "~", "NOT_MET": "✗"}[criterion['status']]
        print(f"  {status_symbol} {criterion['criterion']}")
        print(f"    Evidence: {criterion['evidence']}")

    print(f"\nWeaknesses:")
    for weakness in result['weaknesses']:
        print(f"  ✗ {weakness}")

    print(f"\nRevision Instructions:")
    for i, instruction in enumerate(result['revision_instructions'], 1):
        print(f"  {i}. {instruction}")

    print(f"\nFeedback: {result['feedback']}")


async def example_quality_checker():
    """Example of using the QualityChecker independently."""
    print("\n\n")
    print("=" * 80)
    print("EXAMPLE 3: Quality Checker for Individual Artifacts")
    print("=" * 80)

    artifact = Artifact(
        id="art_003",
        task_id="task_003",
        uri="file:///tmp/config.json",
        type="data",
        mime_type="application/json",
        size_bytes=450
    )

    content = {
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "production_db"
        },
        "cache": {
            "enabled": True,
            "ttl": 3600
        }
    }

    # In production, you'd call:
    # checker = QualityChecker()
    # report = await checker.check_quality(artifact, content)

    # Simulated report
    report = {
        "artifact_id": "art_003",
        "quality_score": 82.0,
        "static_score": 95.0,
        "llm_score": 74.0,
        "passed": True,
        "quality_level": "GOOD",
        "static_checks": {
            "file_exists": True,
            "content_not_empty": True,
            "size_reasonable": True,
            "format_valid": True,
            "structure_valid": True
        },
        "llm_checks": {
            "tone_consistency": True,
            "clarity": True,
            "professional_standards": True
        },
        "strengths": [
            "Valid JSON structure",
            "Clear configuration hierarchy",
            "Reasonable default values"
        ],
        "weaknesses": [
            "Missing documentation/comments",
            "No validation schema defined"
        ],
        "recommendations": [
            "Add JSON schema for validation",
            "Include environment-specific configs",
            "Document each configuration option"
        ]
    }

    print("\n" + "=" * 40)
    print("QUALITY REPORT")
    print("=" * 40)
    print(f"Artifact: {report['artifact_id']}")
    print(f"Quality Score: {report['quality_score']}/100")
    print(f"Quality Level: {report['quality_level']}")
    print(f"Status: {'PASSED' if report['passed'] else 'FAILED'}")

    print(f"\nScore Breakdown:")
    print(f"  Static Checks (40%): {report['static_score']}/100")
    print(f"  LLM Checks (60%): {report['llm_score']}/100")

    print(f"\nStatic Checks:")
    for check, result in report['static_checks'].items():
        symbol = "✓" if result else "✗"
        print(f"  {symbol} {check.replace('_', ' ').title()}")

    print(f"\nStrengths:")
    for strength in report['strengths']:
        print(f"  ✓ {strength}")

    print(f"\nWeaknesses:")
    for weakness in report['weaknesses']:
        print(f"  ⚠ {weakness}")

    print(f"\nRecommendations:")
    for rec in report['recommendations']:
        print(f"  → {rec}")


async def main():
    """Run all examples."""
    await example_successful_review()
    await example_revision_needed()
    await example_quality_checker()

    print("\n\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print("""
The Enhanced Reviewer Module provides:

1. ✓ Comprehensive review with chain-of-thought reasoning
2. ✓ Hybrid quality checking (40% static, 60% LLM)
3. ✓ Self-correction loop with max 2 iterations
4. ✓ Detailed requirement coverage tracking
5. ✓ Specific, actionable revision instructions
6. ✓ Quality scoring (0-100) with level classification
7. ✓ Rich feedback and recommendations

Quality Levels:
  - 90-100: EXCELLENT
  - 80-89:  GOOD
  - 70-79:  ACCEPTABLE (passes review)
  - 60-69:  MARGINAL (revision recommended)
  - 0-59:   POOR (revision required)

Usage:
  reviewer = Reviewer(max_iterations=2)
  result = await reviewer.review_with_correction_loop(state, user_memory)

See src/reviewer/README.md for full documentation.
    """)


if __name__ == "__main__":
    asyncio.run(main())
