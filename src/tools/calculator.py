from typing import Any, Dict
import math
from src.tools.base import BaseTool, ToolMetadata
from src.utils.logger import logger

class CalculatorTool(BaseTool):
    """Tool for performing mathematical calculations."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="calculator",
            description=(
                "Performs mathematical calculations and evaluates mathematical expressions. "
                "USE THIS TOOL FOR: Arithmetic, algebra, trigonometry, statistical calculations. "
                "DO NOT USE FOR: Searching information, generating content, writing code. "
                "SUPPORTS: Basic operations (+, -, *, /), powers, roots, trigonometric functions."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "Mathematical expression to evaluate (e.g., '2 + 2', 'sqrt(16)', 'sin(pi/2)')"},
                    "precision": {"type": "integer", "description": "Number of decimal places for result", "default": 2}
                },
                "required": ["expression"]
            },
            returns={"type": "number", "description": "Result of the calculation"}
        )

    async def execute(self, expression: str, precision: int = 2, **kwargs) -> float:
        logger.info(f"Calculating: {expression}")

        # Safe mathematical namespace
        safe_dict = {
            'abs': abs,
            'round': round,
            'min': min,
            'max': max,
            'sum': sum,
            'pow': pow,
            'sqrt': math.sqrt,
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'pi': math.pi,
            'e': math.e,
            'log': math.log,
            'log10': math.log10,
            'exp': math.exp,
            'factorial': math.factorial,
        }

        try:
            # Evaluate expression in safe environment
            result = eval(expression, {"__builtins__": {}}, safe_dict)
            
            # Round to specified precision
            if isinstance(result, (int, float)):
                result = round(result, precision)
            
            logger.info(f"Result: {result}")
            return result
        except Exception as e:
            logger.error(f"Calculation error: {str(e)}")
            raise ValueError(f"Invalid mathematical expression: {expression}. Error: {str(e)}")
