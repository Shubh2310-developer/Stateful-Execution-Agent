EXECUTION_TEMPLATE = """STEP TO EXECUTE:
{step_definition}

INPUTS AVAILABLE:
{available_artifacts}

TOOLS AVAILABLE:
{tool_list}

USER PREFERENCES:
{user_preferences}

Perform the necessary actions using the available tools and return the result as a JSON object containing:
1. 'action': The name of the tool to invoke.
2. 'parameters': The arguments for the tool.
3. 'reasoning': Your explanation for this specific choice.
4. 'confidence': Your confidence level (0.0 to 1.0).
"""
