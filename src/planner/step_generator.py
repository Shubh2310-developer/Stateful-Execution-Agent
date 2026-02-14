from typing import List, Dict, Any, Optional
from src.core.types import Step, UserMemory
from src.llm.groq_client import groq_client
from src.llm.response_parser import ResponseParser
from src.llm.prompt_builder import prompt_builder
from src.utils.logger import logger

class StepGenerator:
    """Generates an ordered list of atomic steps to achieve a parsed goal."""

    async def generate(
        self,
        goal: Dict[str, Any],
        tool_list: List[str],
        memory_context: Optional[UserMemory] = None
    ) -> List[Step]:
        logger.info("Generating execution steps...")

        # Use the global prompt_builder instance and include few-shot examples
        messages = prompt_builder.build_planner_prompt(
            goal=goal.get("primary_objective", str(goal)),
            tool_list=tool_list,
            user_preferences=getattr(memory_context, 'preferences', None) if memory_context else None,
            constraints=goal.get("constraints"),
            include_examples=True
        )

        response_text = await groq_client.generate_response(messages)
        plan_data = ResponseParser.parse_json_response(response_text)

        steps = []
        for step_dict in plan_data.get("steps", []):
            # Ensure step_id vs id compatibility
            if 'step_id' in step_dict and 'id' not in step_dict:
                step_dict['id'] = step_dict.pop('step_id')
            steps.append(Step(**step_dict))

        logger.debug(f"Generated {len(steps)} steps.")
        return steps
