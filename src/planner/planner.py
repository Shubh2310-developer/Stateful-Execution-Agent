from typing import List, Dict, Any, Optional
from uuid import uuid4
from src.core.types import Plan, Step, UserMemory, Goal
from src.planner.goal_parser import GoalParser
from src.planner.step_generator import StepGenerator
from src.planner.dependency_analyzer import DependencyAnalyzer
from src.planner.plan_validator import PlanValidator
from src.planner.adaptive_planner import AdaptivePlanner
from src.utils.logger import logger
from datetime import datetime

class Planner:
    """Orchestrates the decomposition of goals into validated execution plans."""

    def __init__(self):
        self.goal_parser = GoalParser()
        self.step_generator = StepGenerator()
        self.dependency_analyzer = DependencyAnalyzer()
        self.plan_validator = PlanValidator()
        self.adaptive_planner = AdaptivePlanner()

    async def create_plan(
        self,
        raw_goal: str,
        available_tools: List[str],
        user_memory: Optional[UserMemory] = None,
        context: Optional[Dict[str, Any]] = None,
        max_retries: int = 2
    ) -> Plan:
        """
        Main entry point for creating a validated execution plan.
        Includes a retry loop for self-correction if validation fails.
        """
        logger.info(f"Creating plan for goal: {raw_goal[:50]}...")

        # 1. Parse and refine the goal
        parsed_goal_data = await self.goal_parser.parse(raw_goal, context)

        # 1.5 Prepare adaptive context from memory
        adaptive_context = await self.adaptive_planner.prepare_adaptive_context(
            goal_text=parsed_goal_data.get("primary_objective", raw_goal),
            user_memory=user_memory
        )

        attempts = 0
        last_feedback = ""

        while attempts <= max_retries:
            attempts += 1
            logger.info(f"Planning attempt {attempts}/{max_retries + 1}")

            # 2. Generate initial sequence of steps
            # We override memory_context pieces with processed adaptive context
            steps = await self.step_generator.generate(
                goal=parsed_goal_data,
                tool_list=available_tools,
                memory_context=user_memory,
                feedback=last_feedback if attempts > 1 else None,
                adaptive_lessons=adaptive_context.get("lessons_learned")
            )

            # 3. Analyze and sort dependencies (Topological Sort)
            try:
                sorted_steps = self.dependency_analyzer.analyze(steps)
            except Exception as e:
                logger.warning(f"Dependency analysis failed: {str(e)}")
                last_feedback = f"Step dependencies are invalid: {str(e)}"
                continue

            # 4. Create Plan object
            task_id = context.get("task_id") if context else f"task_{uuid4().hex[:8]}"
            plan = Plan(
                task_id=task_id,
                steps=sorted_steps,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )

            # 5. Semantic Validation via LLM
            audit_result = await self.plan_validator.validate(plan, parsed_goal_data, available_tools)

            if audit_result.get("isValid"):
                logger.info(f"Plan created and validated successfully: {task_id}")
                return plan
            else:
                last_feedback = audit_result.get("feedback", "Unknown validation error")
                logger.warning(f"Plan validation failed (Attempt {attempts}): {last_feedback}")

                if attempts <= max_retries:
                    logger.info("Retrying plan generation with feedback...")
                    # Future enhancement: feed last_feedback back into StepGenerator

        raise Exception(f"Failed to generate a valid plan after {attempts} attempts. Last feedback: {last_feedback}")
