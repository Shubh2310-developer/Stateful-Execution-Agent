from typing import List, Dict, Any
from src.core.types import Step, Plan
from src.core.exceptions import ValidationError
from src.llm.groq_client import groq_client
from src.llm.prompt_builder import prompt_builder
from src.llm.response_parser import ResponseParser
from src.utils.logger import logger

class PlanValidator:
    """Validates that a generated plan is complete, feasible, and logically sound."""

    async def validate(self, plan: Plan, goal: Dict[str, Any], available_tools: List[str]) -> Dict[str, Any]:
        """
        Performs both structural and LLM-based semantic validation.
        Returns a dict with 'isValid', 'feedback', and 'risks'.
        """
        logger.info(f"Validating plan for task: {plan.task_id}")

        if not plan.steps:
            return {"isValid": False, "feedback": "Plan contains no steps.", "risks": ["Empty plan"]}

        # 1. Structural Validation
        step_ids = [s.step_id for s in plan.steps]
        if len(step_ids) != len(set(step_ids)):
            return {"isValid": False, "feedback": "Plan contains duplicate step IDs.", "risks": ["ID collision"]}

        # Check for invalid tool references
        missing_tools = []
        for step in plan.steps:
            for tool in step.tools:
                if tool not in available_tools:
                    missing_tools.append(tool)

        if missing_tools:
            logger.warning(f"Plan references missing tools: {set(missing_tools)}")

        # 2. Semantic Validation via LLM
        steps_dict = [s.dict() for s in plan.steps]
        messages = prompt_builder.build_plan_validator_prompt(goal, steps_dict, available_tools)

        try:
            response_text = await groq_client.generate_response(messages)
            audit_result = ResponseParser.parse_json_response(response_text)

            # Log the Chain-of-Thought reasoning
            reasoning = audit_result.get("reasoning", "No reasoning provided.")
            logger.info(f"Plan Validator Reasoning: {reasoning}")

            logger.info(f"Plan audit result: {'Valid' if audit_result.get('isValid') else 'Invalid'}")
            return audit_result
        except Exception as e:
            logger.error(f"Plan semantic validation failed: {str(e)}")
            # Fallback to structural validity if LLM fails
            return {
                "isValid": True,
                "feedback": "Semantic validation failed, but structural check passed.",
                "risks": ["Validation bypass"]
            }
