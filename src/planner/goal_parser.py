from typing import Dict, Any, Optional
from src.llm.groq_client import groq_client
from src.llm.prompt_builder import prompt_builder
from src.llm.response_parser import ResponseParser
from src.utils.logger import logger

class GoalParser:
    """Parses and refines high-level user goals into structured outcomes."""

    async def parse(self, raw_goal: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        logger.info(f"Parsing raw goal: {raw_goal[:50]}...")

        messages = prompt_builder.build_goal_parser_prompt(raw_goal, context)

        response_text = await groq_client.generate_response(messages)
        parsed_goal = ResponseParser.parse_json_response(response_text)

        # Log the Chain-of-Thought reasoning
        reasoning = parsed_goal.get("reasoning", "No reasoning provided.")
        logger.info(f"Goal Parser Reasoning: {reasoning}")

        logger.debug(f"Parsed goal: {parsed_goal.get('primary_objective')}")
        return parsed_goal
