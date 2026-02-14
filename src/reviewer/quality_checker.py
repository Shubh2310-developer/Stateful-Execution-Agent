from typing import Any, Dict, Optional
from src.core.types import Artifact
from src.llm.groq_client import groq_client
from src.llm.response_parser import ResponseParser
from src.utils.logger import logger

class QualityChecker:
    """Performs deep quality analysis on execution artifacts."""

    async def check_quality(self, artifact: Artifact, content: Any) -> Dict[str, Any]:
        logger.info(f"Checking quality for artifact: {artifact.id}")

        messages = prompt_builder.build_quality_checker_prompt(
            artifact_type=artifact.type,
            artifact_id=artifact.id,
            content=str(content)[:5000]
        )

        try:
            response_text = await groq_client.generate_response(messages)
            quality_report = ResponseParser.parse_json_response(response_text)

            # Log the Chain-of-Thought reasoning
            reasoning = quality_report.get("reasoning", "No reasoning provided.")
            logger.info(f"Quality Checker Reasoning: {reasoning}")

            return quality_report
        except Exception as e:
            logger.error(f"Quality check failed: {str(e)}")
            return {"quality_score": 0.0, "error": str(e)}
