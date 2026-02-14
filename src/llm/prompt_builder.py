import os
from typing import List, Dict, Any, Optional
from jinja2 import Environment, FileSystemLoader, select_autoescape
from src.core.types import Step, TaskState, Plan

# Fallback for UserMemory if not in types
try:
    from src.core.types import UserMemory
except ImportError:
    UserMemory = Any

class PromptBuilder:
    def __init__(self, template_dir: Optional[str] = None):
        if not template_dir:
            # Default to the src root to allow relative paths to planner/executor prompts
            template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(['html', 'xml']),
            trim_blocks=True,
            lstrip_blocks=True
        )

    def build_planner_prompt(
        self,
        goal: str,
        tool_list: List[str],
        user_preferences: Optional[Dict[str, Any]] = None,
        constraints: Optional[List[str]] = None,
        include_examples: bool = True
    ) -> List[Dict[str, str]]:
        """Builds the planner prompt using Jinja2 templates."""
        system_template = self.env.get_template("planner/prompts/planner_system.j2")
        user_template = self.env.get_template("planner/prompts/planner_user.j2")

        few_shot_examples = None
        if include_examples:
            try:
                from src.planner.prompts.few_shot_examples import FEW_SHOT_EXAMPLES
                few_shot_examples = FEW_SHOT_EXAMPLES
            except ImportError:
                pass

        system_content = system_template.render()
        user_content = user_template.render(
            goal=goal,
            tool_list=tool_list,
            user_preferences=user_preferences,
            constraints=constraints,
            few_shot_examples=few_shot_examples
        )

        return [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content}
        ]

    def build_replanning_prompt(
        self,
        goal: str,
        plan: Plan,
        feedback: str,
        available_artifacts: Dict[str, Any],
        include_examples: bool = True
    ) -> List[Dict[str, str]]:
        """Builds the replanning prompt for plan adjustments."""
        system_template = self.env.get_template("planner/prompts/planner_system.j2")
        user_template = self.env.get_template("planner/prompts/planner_replanning_user.j2")

        system_content = system_template.render()

        # Extract steps for the template
        steps_info = []
        for s in plan.steps:
            steps_info.append({
                "id": s.id,
                "description": s.description,
                "status": s.status.value if hasattr(s.status, 'value') else str(s.status)
            })

        user_content = user_template.render(
            goal=goal,
            steps=steps_info,
            feedback=feedback,
            available_artifacts=available_artifacts
        )

        return [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content}
        ]

    def build_executor_prompt(
        self,
        step: Step,
        available_artifacts: Dict[str, Any],
        tool_list: List[str],
        user_preferences: Optional[Dict[str, Any]] = None,
        include_examples: bool = True
    ) -> List[Dict[str, str]]:
        """Builds the executor prompt using Jinja2 templates."""
        system_template = self.env.get_template("executor/prompts/executor_system.j2")
        user_template = self.env.get_template("executor/prompts/executor_user.j2")

        few_shot_examples = None
        if include_examples:
            try:
                from src.executor.prompts.few_shot_examples import EXECUTION_EXAMPLES
                few_shot_examples = EXECUTION_EXAMPLES
            except ImportError:
                pass

        system_content = system_template.render()

        # Convert Pydantic model to dict for Jinja2
        step_dict = step.dict() if hasattr(step, 'dict') else step

        user_content = user_template.render(
            step_definition=step_dict,
            available_artifacts=available_artifacts,
            tool_list=tool_list,
            user_preferences=user_preferences,
            few_shot_examples=few_shot_examples
        )

        return [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content}
        ]

    def build_validator_prompt(
        self,
        step_description: str,
        success_criteria: List[str],
        step_output: Any
    ) -> List[Dict[str, str]]:
        """Builds the validation prompt for quality assurance."""
        system_template = self.env.get_template("executor/prompts/validator_system.j2")
        user_template = self.env.get_template("executor/prompts/validator_user.j2")

        system_content = system_template.render()
        user_content = user_template.render(
            step_description=step_description,
            success_criteria=success_criteria,
            step_output=step_output
        )

        return [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content}
        ]

    def build_goal_parser_prompt(
        self,
        raw_goal: str,
        context: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, str]]:
        """Builds the goal parsing prompt."""
        system_template = self.env.get_template("planner/prompts/goal_parser_system.j2")
        user_template = self.env.get_template("planner/prompts/goal_parser_user.j2")

        system_content = system_template.render()
        user_content = user_template.render(
            raw_goal=raw_goal,
            context=context
        )

        return [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content}
        ]

# Global instance for easy import
prompt_builder = PromptBuilder()
