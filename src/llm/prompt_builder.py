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
        lessons_learned: Optional[List[str]] = None,
        past_experiences: Optional[List[str]] = None,
        feedback: Optional[str] = None,
        include_examples: bool = True
    ) -> List[Dict[str, str]]:
        """Builds the planner prompt using Jinja2 templates."""
        system_template = self.env.get_template("planner/prompts/planner_system.j2")
        user_template = self.env.get_template("planner/prompts/planner_user.j2")

        few_shot_examples = None
        if include_examples:
            try:
                from src.planner.prompts.few_shot_examples import PLANNER_EXAMPLES
                few_shot_examples = PLANNER_EXAMPLES
            except ImportError:
                pass

        system_content = system_template.render()
        user_content = user_template.render(
            goal=goal,
            tool_list=tool_list,
            user_preferences=user_preferences,
            constraints=constraints,
            lessons_learned=lessons_learned,
            past_experiences=past_experiences,
            feedback=feedback,
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
        context: Optional[Dict[str, Any]] = None,
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
            context=context,
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

    def build_plan_validator_prompt(
        self,
        goal: Dict[str, Any],
        steps: List[Dict[str, Any]],
        available_tools: List[str],
        include_examples: bool = True
    ) -> List[Dict[str, str]]:
        """Builds the plan validation prompt for quality auditing."""
        system_template = self.env.get_template("planner/prompts/validator_system.j2")
        user_template = self.env.get_template("planner/prompts/validator_user.j2")

        few_shot_examples = None
        if include_examples:
            try:
                from src.planner.prompts.few_shot_examples import PLAN_VALIDATOR_EXAMPLES
                few_shot_examples = PLAN_VALIDATOR_EXAMPLES
            except ImportError:
                pass

        system_content = system_template.render()
        user_content = user_template.render(
            goal=goal,
            steps=steps,
            available_tools=available_tools,
            few_shot_examples=few_shot_examples
        )

        return [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content}
        ]

    def build_goal_parser_prompt(
        self,
        raw_goal: str,
        context: Optional[Dict[str, Any]] = None,
        include_examples: bool = True
    ) -> List[Dict[str, str]]:
        """Builds the goal parsing prompt."""
        system_template = self.env.get_template("planner/prompts/goal_parser_system.j2")
        user_template = self.env.get_template("planner/prompts/goal_parser_user.j2")

        few_shot_examples = None
        if include_examples:
            try:
                from src.planner.prompts.few_shot_examples import GOAL_PARSER_EXAMPLES
                few_shot_examples = GOAL_PARSER_EXAMPLES
            except ImportError:
                pass

        system_content = system_template.render()
        user_content = user_template.render(
            raw_goal=raw_goal,
            context=context,
            few_shot_examples=few_shot_examples
        )

        return [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content}
        ]

    def build_reviewer_prompt(
        self,
        goal: Dict[str, Any],
        plan_steps: List[Dict[str, Any]],
        artifacts: List[Dict[str, Any]]
    ) -> List[Dict[str, str]]:
        """Builds the end-to-end review prompt."""
        system_template = self.env.get_template("reviewer/prompts/reviewer_system.j2")
        user_template = self.env.get_template("reviewer/prompts/reviewer_user.j2")

        system_content = system_template.render()
        user_content = user_template.render(
            goal=goal,
            plan_steps=plan_steps,
            artifacts=artifacts
        )

        return [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content}
        ]

    def build_quality_checker_prompt(
        self,
        artifact_type: str,
        artifact_id: str,
        content: Any
    ) -> List[Dict[str, str]]:
        """Builds the deep artifact quality check prompt."""
        system_template = self.env.get_template("reviewer/prompts/quality_checker_system.j2")
        user_template = self.env.get_template("reviewer/prompts/quality_checker_user.j2")

        system_content = system_template.render()
        user_content = user_template.render(
            artifact_type=artifact_type,
            artifact_id=artifact_id,
            content=content
        )

        return [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content}
        ]

    def build_summarizer_prompt(
        self,
        text: str,
        focus: Optional[str] = None
    ) -> List[Dict[str, str]]:
        """Builds the summarizer tool prompt."""
        system_template = self.env.get_template("tools/document/prompts/summarizer_system.j2")
        user_template = self.env.get_template("tools/document/prompts/summarizer_user.j2")

        system_content = system_template.render()
        user_content = user_template.render(
            text=text,
            focus=focus
        )

        return [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content}
        ]

    def build_correction_prompt(
        self,
        step: Step,
        previous_action: str,
        previous_params: Dict[str, Any],
        previous_output: Any,
        issues: List[str],
        available_artifacts: Dict[str, Any],
        tool_list: List[str],
        user_preferences: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, str]]:
        """Builds the correction prompt for self-correction loops."""
        system_template = self.env.get_template("executor/prompts/executor_system.j2")
        user_template = self.env.get_template("executor/prompts/correction_user.j2")

        system_content = system_template.render()

        # Convert Pydantic model to dict for Jinja2
        step_dict = step.dict() if hasattr(step, 'dict') else step

        user_content = user_template.render(
            step_definition=step_dict,
            previous_action=previous_action,
            previous_params=previous_params,
            previous_output=previous_output,
            issues=issues,
            available_artifacts=available_artifacts,
            tool_list=tool_list,
            user_preferences=user_preferences
        )

        return [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content}
        ]

    def build_reflection_prompt(
        self,
        goal: str,
        status: str,
        logs: List[Dict[str, Any]],
        artifacts: List[Dict[str, Any]],
        feedback: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, str]]:
        """Builds the deep reflection prompt."""
        system_template = self.env.get_template("memory/learning/prompts/reflection_system.j2")
        user_template = self.env.get_template("memory/learning/prompts/reflection_user.j2")

        system_content = system_template.render()
        user_content = user_template.render(
            goal=goal,
            status=status,
            logs=logs,
            artifacts=artifacts,
            feedback=feedback
        )

        return [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content}
        ]

    def build_adaptation_prompt(
        self,
        goal: str,
        status: str,
        steps: List[Dict[str, Any]],
        artifacts: List[Dict[str, Any]],
        logs: Optional[List[Dict[str, Any]]] = None,
        feedback: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, str]]:
        """Builds the adaptation/learning prompt."""
        system_template = self.env.get_template("memory/learning/prompts/adaptation_system.j2")
        user_template = self.env.get_template("memory/learning/prompts/adaptation_user.j2")

        system_content = system_template.render()
        user_content = user_template.render(
            goal=goal,
            status=status,
            steps=steps,
            artifacts=artifacts,
            logs=logs,
            feedback=feedback
        )

        return [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content}
        ]

# Global instance for easy import
prompt_builder = PromptBuilder()
