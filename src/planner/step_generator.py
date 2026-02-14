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
        memory_context: Optional[UserMemory] = None,
        feedback: Optional[str] = None,
        adaptive_lessons: Optional[List[str]] = None
    ) -> List[Step]:
        logger.info("Generating execution steps...")

        # prioritize lessons from adaptive_planner if provided
        past_experiences = adaptive_lessons
        lessons_learned = None
        if not past_experiences and memory_context:
            lessons_learned = getattr(memory_context, 'historical_patterns', None)

        # Use the global prompt_builder instance and include few-shot examples
        messages = prompt_builder.build_planner_prompt(
            goal=goal.get("primary_objective", str(goal)),
            tool_list=tool_list,
            user_preferences=getattr(memory_context, 'preferences', None) if memory_context else None,
            constraints=goal.get("constraints"),
            lessons_learned=lessons_learned,
            past_experiences=past_experiences,
            feedback=feedback,
            include_examples=True
        )

        response_text = await groq_client.generate_response(messages)
        plan_data = ResponseParser.parse_json_response(response_text)

        # Log the Chain-of-Thought reasoning
        reasoning = plan_data.get("reasoning", "No reasoning provided.")
        logger.info(f"Planner Reasoning: {reasoning}")

        steps = []
        for i, step_dict in enumerate(plan_data.get("steps", []), 1):
            # Ensure step_id vs id compatibility
            if 'id' in step_dict and 'step_id' not in step_dict:
                step_dict['step_id'] = step_dict.pop('id')

            # Default order if not provided
            if 'order' not in step_dict:
                step_dict['order'] = i

            # Map tools_needed to tools if present
            if 'tools_needed' in step_dict and 'tools' not in step_dict:
                step_dict['tools'] = step_dict.pop('tools_needed')
            elif 'action' in step_dict and not step_dict.get('tools'):
                # Ensure the 'action' tool is in the 'tools' list for compatibility
                step_dict['tools'] = [step_dict['action']]

            steps.append(Step(**step_dict))

        logger.debug(f"Generated {len(steps)} steps.")
        return steps
