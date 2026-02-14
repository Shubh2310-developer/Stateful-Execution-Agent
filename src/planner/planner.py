from typing import List, Dict, Any, Optional
from uuid import uuid4
from src.core.types import Plan, Step, UserMemory
from src.planner.goal_parser import GoalParser
from src.planner.step_generator import StepGenerator
from src.planner.dependency_analyzer import DependencyAnalyzer
from src.planner.plan_validator import PlanValidator
from src.utils.logger import logger

class Planner:
    """Orchestrates the decomposition of goals into validated execution plans."""

    def __init__(self):
        self.goal_parser = GoalParser()
        self.step_generator = StepGenerator()
        self.dependency_analyzer = DependencyAnalyzer()
        self.plan_validator = PlanValidator()

    async def create_plan(
        self,
        raw_goal: str,
        available_tools: List[str],
        user_memory: Optional[UserMemory] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Plan:
        logger.info(f"Creating plan for goal: {raw_goal[:50]}...")

        # 1. Parse and refine the goal
        parsed_goal = await self.goal_parser.parse(raw_goal, context)

        # 2. Generate initial sequence of steps
        steps = await self.step_generator.generate(parsed_goal, available_tools, user_memory)

        # 3. Analyze and sort dependencies
        sorted_steps = self.dependency_analyzer.analyze(steps)

        # 4. Create Plan object
        task_id = f"task_{uuid4().hex[:8]}"
        plan = Plan(
            task_id=task_id,
            goal_summary=parsed_goal.get("primary_objective", raw_goal),
            steps=sorted_steps,
            total_estimated_duration_minutes=sum(s.estimated_duration_minutes or 0 for s in sorted_steps),
            risk_assessment=parsed_goal.get("risk_assessment", "low")
        )

        # 5. Validate the final plan
        self.plan_validator.validate(plan, available_tools)

        logger.info(f"Plan created successfully: {task_id}")
        return plan
