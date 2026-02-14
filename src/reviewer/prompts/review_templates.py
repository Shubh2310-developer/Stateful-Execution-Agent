REVIEW_TEMPLATE = """You are a senior reviewer. Please evaluate the following task execution:

TASK GOAL: {goal}
PLAN STEPS: {plan_summary}
ARTIFACTS PRODUCED: {artifact_list}

Analyze the overall success and quality. Determine if the goal was fully achieved and if the artifacts meet production standards.

Return your review as a JSON object matching the Review schema.
"""

REVISION_TEMPLATE = """The previous execution was not fully successful or high quality.

ISSUES IDENTIFIED:
{issues}

RECOMMENDATIONS:
{recommendations}

Please propose a revision plan to address these points.
"""
