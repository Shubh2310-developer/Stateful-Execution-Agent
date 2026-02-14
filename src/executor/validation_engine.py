from typing import Any, Dict, List, Optional
from src.core.types import Step, Artifact
from src.llm.groq_client import groq_client
from src.llm.prompt_builder import prompt_builder
from src.llm.response_parser import ResponseParser
from src.utils.logger import logger

class ValidationEngine:
    """Validates execution outputs against step success criteria using LLM."""

    async def validate_output(
        self,
        step: Step,
        artifact: Artifact,
        artifact_content: Any
    ) -> Dict[str, Any]:
        # step_id and success_criteria might have different names in the actual Step model
        step_id = getattr(step, 'id', getattr(step, 'step_id', 'unknown'))
        criteria = getattr(step, 'success_criteria', [])
        description = getattr(step, 'description', '')

        logger.info(f"Validating output for step {step_id}...")

        messages = prompt_builder.build_validator_prompt(
            step_description=description,
            success_criteria=criteria,
            step_output=artifact_content
        )

        try:
            response_text = await groq_client.generate_response(messages)
            validation_result = ResponseParser.parse_json_response(response_text)

            # Log the Chain-of-Thought reasoning
            reasoning = validation_result.get("reasoning", "No reasoning provided.")
            logger.info(f"Validator Reasoning for {step_id}: {reasoning}")

            logger.info(f"Validation result for {step_id}: {'PASSED' if validation_result.get('passed') else 'FAILED'}")
            return validation_result
        except Exception as e:
            logger.error(f"Validation failed due to error: {str(e)}")
            return {
                "passed": False,
                "reasoning": f"Validation engine error: {str(e)}",
                "quality_score": 0.0,
                "issues": ["Validation engine failure"]
            }
