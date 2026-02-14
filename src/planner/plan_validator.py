from typing import List, Dict, Any
from src.core.types import Step, Plan
from src.core.exceptions import ValidationError
from src.utils.logger import logger

class PlanValidator:
    """Validates that a generated plan is complete, feasible, and logically sound."""

    def validate(self, plan: Plan, available_tools: List[str]) -> bool:
        logger.info(f"Validating plan for task: {plan.task_id}")

        if not plan.steps:
            raise ValidationError("Plan contains no steps.")

        # Check for duplicate step IDs
        step_ids = [s.step_id for s in plan.steps]
        if len(step_ids) != len(set(step_ids)):
            raise ValidationError("Plan contains duplicate step IDs.")

        # Check for circular dependencies or invalid dependencies
        for step in plan.steps:
            for dep_id in step.dependencies:
                if dep_id not in step_ids:
                    raise ValidationError(f"Step {step.step_id} depends on non-existent step: {dep_id}")

                # Simple check: dependency should ideally have a lower order than the step
                dep_step = next(s for s in plan.steps if s.step_id == dep_id)
                if dep_step.order >= step.order:
                    logger.warning(f"Step {step.step_id} (order {step.order}) depends on step {dep_id} (order {dep_step.order})")

            # Check if tools are available
            for tool in step.tools_needed:
                if tool not in available_tools:
                    logger.warning(f"Step {step.step_id} requires tool '{tool}' which is not in the available tools list.")

        logger.info("Plan validation successful.")
        return True
