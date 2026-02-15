from typing import Any, Dict, Optional
from src.tools.base import BaseTool, ToolMetadata
from src.utils.logger import logger

class CodeGeneratorTool(BaseTool):
    """Tool for generating code in various programming languages."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="code_generator",
            description=(
                "Generates code snippets, functions, or scripts in Python, JavaScript, or other languages. "
                "USE THIS TOOL FOR: Writing functions, creating scripts, generating code examples. "
                "DO NOT USE FOR: Searching for code, writing documentation, performing calculations. "
                "RETURNS: Complete, executable code with proper syntax."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "description": {"type": "string", "description": "What the code should do"},
                    "language": {"type": "string", "description": "Programming language (python, javascript, etc.)", "default": "python"},
                    "include_comments": {"type": "boolean", "description": "Whether to include explanatory comments", "default": True},
                    "include_tests": {"type": "boolean", "description": "Whether to include test cases", "default": False}
                },
                "required": ["description"]
            },
            returns={"type": "string", "description": "Generated code"}
        )

    async def execute(self, description: str, language: str = "python", include_comments: bool = True, include_tests: bool = False, **kwargs) -> str:
        logger.info(f"Generating {language} code for: {description}")

        # Generate code based on description
        # This is a simple template - in production, you'd use an LLM or code generation service
        
        if "factorial" in description.lower():
            code = """def factorial(n):
    \"\"\"Calculate the factorial of a non-negative integer.
    
    Args:
        n: Non-negative integer
        
    Returns:
        Factorial of n
    \"\"\"
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)
"""
        elif "add" in description.lower() or "sum" in description.lower():
            code = """def add_numbers(a, b):
    \"\"\"Add two numbers together.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        Sum of a and b
    \"\"\"
    return a + b
"""
        elif "hello" in description.lower():
            code = """def hello_world():
    \"\"\"Print hello world message.\"\"\"
    print("Hello, World!")
    return "Hello, World!"
"""
        else:
            # Generic function template
            code = f"""def generated_function():
    \"\"\"
    {description}
    \"\"\"
    # TODO: Implement logic for: {description}
    pass
"""

        if include_tests and language == "python":
            code += """

# Test cases
if __name__ == "__main__":
    # Add your test cases here
    pass
"""

        return code
