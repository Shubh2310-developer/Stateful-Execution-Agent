PLANNING_TEMPLATE = """GOAL: {goal}

CONTEXT:
- Available Tools: {tool_list}
- User Preferences: {user_preferences}
- Constraints: {constraints}

Generate a detailed execution plan following the standard schema. Return ONLY the JSON object.
"""

REPLANNING_TEMPLATE = """ORIGINAL GOAL: {goal}
CURRENT STATE: {current_state}
FAILURE REASON / FEEDBACK: {feedback}

Update the remaining steps of the plan to account for this information. Ensure the path to the original goal remains clear.
"""
