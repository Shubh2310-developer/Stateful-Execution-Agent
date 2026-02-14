from typing import Any, Dict, Optional
from src.core.types import Artifact
from src.llm.groq_client import groq_client
from src.llm.response_parser import ResponseParser
from src.utils.logger import logger

class QualityChecker:
    """Performs deep quality analysis on execution artifacts."""

    async def check_quality(self, artifact: Artifact, content: Any) -> Dict[str, Any]:
        logger.info(f"Checking quality for artifact: {artifact.artifact_id}")

        system_prompt = """You are a senior quality assurance engineer.
Your task is to perform a deep quality check on the provided artifact.

Analyze:
1. Technical accuracy
2. Adherence to professional standards
3. Clarity and coherence
4. Potential improvements

Return your evaluation as a JSON object:
{
  "quality_score": float (0.0 to 1.0),
  "strengths": list[str],
  "weaknesses": list[str],
  "recommendations": list[str]
}"""

        user_content = f"Artifact Type: {artifact.type}\nContent: {str(content)[:5000]}"

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ]

        try:
            response_text = await groq_client.generate_response(messages)
            return ResponseParser.parse_json_response(response_text)
        except Exception as e:
            logger.error(f"Quality check failed: {str(e)}")
            return {"quality_score": 0.0, "error": str(e)}
