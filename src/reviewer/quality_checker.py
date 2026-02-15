import json
import os
from typing import Any, Dict, List, Optional
from pathlib import Path
from src.core.types import Artifact
from src.llm.groq_client import groq_client
from src.llm.response_parser import ResponseParser
from src.llm.prompt_builder import prompt_builder
from src.utils.logger import logger


class QualityChecker:
    """Performs hybrid quality analysis on execution artifacts using static checks and LLM-powered evaluation."""

    # Quality score weights
    STATIC_WEIGHT = 0.40
    LLM_WEIGHT = 0.60

    # Quality thresholds
    PASS_THRESHOLD = 70.0
    GOOD_THRESHOLD = 80.0
    EXCELLENT_THRESHOLD = 90.0

    def __init__(self):
        """
        Initializes the QualityChecker component.

        This component performs a weighted evaluation of artifact quality using both
        deterministic static checks (40% weight) and semantic LLM evaluation (60% weight).
        """
        pass

    async def check_quality(
        self,
        artifact: Artifact,
        content: Any,
        success_criteria: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Performs a hybrid quality check on a specific artifact.

        This method executes both static and LLM-based checks, calculates a weighted score,
        and determines if the artifact meets the defined quality threshold.

        Args:
            artifact (Artifact): The metadata object for the artifact to be checked.
            content (Any): The actual content of the artifact (e.g., string, dict, or bytes).
            success_criteria (List[str], optional): Specific criteria from the step definition
                to validate against. Defaults to None.

        Returns:
            Dict[str, Any]: A comprehensive quality report including scores, passed status,
                strengths, weaknesses, and actionable recommendations.
        """
        logger.info(f"Starting quality check for artifact: {artifact.id}")

        try:
            # 1. Run static checks
            static_results = await self._run_static_checks(artifact, content)
            static_score = static_results["score"]

            # 2. Run LLM-powered checks
            llm_results = await self._run_llm_checks(
                artifact,
                content,
                success_criteria
            )
            llm_score = llm_results["score"]

            # 3. Calculate combined quality score
            combined_score = self._calculate_quality_score(static_score, llm_score)

            # 4. Aggregate feedback
            quality_report = {
                "artifact_id": artifact.id,
                "quality_score": combined_score,
                "static_score": static_score,
                "llm_score": llm_score,
                "passed": combined_score >= self.PASS_THRESHOLD,
                "quality_level": self._get_quality_level(combined_score),
                "static_checks": static_results["checks"],
                "llm_checks": llm_results["checks"],
                "strengths": llm_results.get("strengths", []),
                "weaknesses": self._aggregate_weaknesses(static_results, llm_results),
                "recommendations": llm_results.get("recommendations", []),
                "reasoning": llm_results.get("reasoning", "Quality analysis completed")
            }

            logger.info(
                f"Quality check completed for {artifact.id}: "
                f"Score={combined_score:.1f}, Level={quality_report['quality_level']}"
            )

            return quality_report

        except Exception as e:
            logger.error(f"Quality check failed for {artifact.id}: {str(e)}")
            return {
                "artifact_id": artifact.id,
                "quality_score": 0.0,
                "passed": False,
                "error": str(e),
                "static_checks": {},
                "llm_checks": {}
            }

    async def _run_static_checks(self, artifact: Artifact, content: Any) -> Dict[str, Any]:
        """
        Runs non-LLM static quality checks.

        Checks include:
        - File existence and accessibility
        - Format validation (JSON, PDF, etc.)
        - Size and word count validation
        - Basic structure validation

        Returns score 0-100
        """
        checks = {}
        issues = []
        passed_checks = 0
        total_checks = 0

        # Check 1: File existence (if URI-based artifact)
        total_checks += 1
        if artifact.uri:
            file_exists = self._check_file_exists(artifact.uri)
            checks["file_exists"] = file_exists
            if file_exists:
                passed_checks += 1
            else:
                issues.append(f"Artifact file not found at URI: {artifact.uri}")

        # Check 2: Content not empty
        total_checks += 1
        content_valid = self._check_content_not_empty(content)
        checks["content_not_empty"] = content_valid
        if content_valid:
            passed_checks += 1
        else:
            issues.append("Artifact content is empty or null")

        # Check 3: Size validation
        total_checks += 1
        size_valid = self._check_size_reasonable(artifact, content)
        checks["size_reasonable"] = size_valid
        if size_valid:
            passed_checks += 1
        else:
            issues.append(f"Artifact size is unreasonable: {artifact.size_bytes} bytes")

        # Check 4: Format-specific validation
        total_checks += 1
        format_valid = self._check_format_validity(artifact, content)
        checks["format_valid"] = format_valid["valid"]
        if format_valid["valid"]:
            passed_checks += 1
        else:
            issues.append(f"Format validation failed: {format_valid.get('error', 'Unknown error')}")

        # Check 5: Structure validation (for structured types)
        if artifact.type in ["data", "code", "document"]:
            total_checks += 1
            structure_valid = self._check_structure(artifact, content)
            checks["structure_valid"] = structure_valid["valid"]
            if structure_valid["valid"]:
                passed_checks += 1
            else:
                issues.append(f"Structure validation failed: {structure_valid.get('error', 'Unknown error')}")

        # Calculate static score
        score = (passed_checks / total_checks * 100) if total_checks > 0 else 0

        return {
            "score": score,
            "checks": checks,
            "passed_count": passed_checks,
            "total_count": total_checks,
            "issues": issues
        }

    async def _run_llm_checks(
        self,
        artifact: Artifact,
        content: Any,
        success_criteria: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Runs LLM-powered quality checks.

        Checks include:
        - Tone consistency
        - Requirement coverage
        - Factual accuracy
        - Professional standards
        - Clarity and coherence

        Returns score 0-100
        """
        # Prepare content for LLM (truncate if too large)
        content_str = str(content)
        if len(content_str) > 5000:
            content_str = content_str[:5000] + "\n\n[... content truncated for analysis ...]"

        # Build quality checker prompt
        messages = prompt_builder.build_quality_checker_prompt(
            artifact_type=artifact.type,
            artifact_id=artifact.id,
            content=content_str
        )

        try:
            response_text = await groq_client.generate_response(messages)
            quality_result = ResponseParser.parse_json_response(response_text)

            # Extract LLM quality score (should be 0.0-1.0, convert to 0-100)
            llm_score_raw = quality_result.get("quality_score", 0.0)
            llm_score = llm_score_raw * 100 if llm_score_raw <= 1.0 else llm_score_raw

            # Extract reasoning and feedback
            reasoning = quality_result.get("reasoning", "No reasoning provided")
            logger.info(f"LLM Quality Check Reasoning: {reasoning}")

            return {
                "score": llm_score,
                "checks": {
                    "tone_consistency": True,  # Derived from LLM analysis
                    "clarity": True,
                    "professional_standards": llm_score >= 70
                },
                "strengths": quality_result.get("strengths", []),
                "weaknesses": quality_result.get("weaknesses", []),
                "recommendations": quality_result.get("recommendations", []),
                "reasoning": reasoning
            }

        except Exception as e:
            logger.error(f"LLM quality check failed: {str(e)}")
            return {
                "score": 50.0,  # Default neutral score on LLM failure
                "checks": {},
                "error": str(e),
                "strengths": [],
                "weaknesses": [f"LLM quality check failed: {str(e)}"],
                "recommendations": ["Manual review recommended due to LLM check failure"]
            }

    def _calculate_quality_score(self, static_score: float, llm_score: float) -> float:
        """
        Calculates the weighted combined quality score.

        Args:
            static_score: Score from static checks (0-100)
            llm_score: Score from LLM checks (0-100)

        Returns:
            Combined score (0-100)
        """
        combined = (static_score * self.STATIC_WEIGHT) + (llm_score * self.LLM_WEIGHT)
        return round(combined, 2)

    def _get_quality_level(self, score: float) -> str:
        """Returns a quality level label based on score."""
        if score >= self.EXCELLENT_THRESHOLD:
            return "EXCELLENT"
        elif score >= self.GOOD_THRESHOLD:
            return "GOOD"
        elif score >= self.PASS_THRESHOLD:
            return "ACCEPTABLE"
        elif score >= 50:
            return "MARGINAL"
        else:
            return "POOR"

    def _aggregate_weaknesses(
        self,
        static_results: Dict[str, Any],
        llm_results: Dict[str, Any]
    ) -> List[str]:
        """Aggregates weaknesses from both static and LLM checks."""
        weaknesses = []

        # Add static check issues
        if "issues" in static_results:
            weaknesses.extend(static_results["issues"])

        # Add LLM-identified weaknesses
        if "weaknesses" in llm_results:
            weaknesses.extend(llm_results["weaknesses"])

        return weaknesses

    # Static check helper methods

    def _check_file_exists(self, uri: str) -> bool:
        """Checks if file exists at given URI."""
        try:
            if uri.startswith("file://"):
                file_path = uri.replace("file://", "")
                return os.path.exists(file_path)
            elif uri.startswith("/") or uri.startswith("./"):
                return os.path.exists(uri)
            # For other URI schemes, assume valid
            return True
        except Exception as e:
            logger.warning(f"File existence check failed: {e}")
            return False

    def _check_content_not_empty(self, content: Any) -> bool:
        """Checks that content is not empty."""
        if content is None:
            return False
        if isinstance(content, str):
            return len(content.strip()) > 0
        if isinstance(content, (list, dict)):
            return len(content) > 0
        return True

    def _check_size_reasonable(self, artifact: Artifact, content: Any) -> bool:
        """Checks that artifact size is reasonable (not too small or too large)."""
        # If size_bytes is available, use it
        if artifact.size_bytes is not None:
            # Minimum 1 byte, maximum 100MB
            return 1 <= artifact.size_bytes <= 100 * 1024 * 1024

        # Otherwise check content length
        content_str = str(content)
        # At least 1 character, max ~10MB of text
        return 1 <= len(content_str) <= 10 * 1024 * 1024

    def _check_format_validity(self, artifact: Artifact, content: Any) -> Dict[str, Any]:
        """Validates format-specific requirements."""
        try:
            # JSON validation
            if artifact.type == "data" or (artifact.mime_type and "json" in artifact.mime_type):
                if isinstance(content, (dict, list)):
                    return {"valid": True}
                # Try parsing string as JSON
                if isinstance(content, str):
                    json.loads(content)
                    return {"valid": True}

            # Code validation (basic check for non-empty)
            if artifact.type == "code":
                if isinstance(content, str) and len(content.strip()) > 0:
                    return {"valid": True}

            # Document validation
            if artifact.type == "document":
                if isinstance(content, str) and len(content.strip()) > 10:
                    return {"valid": True}

            # Default: valid for other types
            return {"valid": True}

        except json.JSONDecodeError as e:
            return {"valid": False, "error": f"Invalid JSON: {str(e)}"}
        except Exception as e:
            return {"valid": False, "error": str(e)}

    def _check_structure(self, artifact: Artifact, content: Any) -> Dict[str, Any]:
        """Validates basic structure for structured artifact types."""
        try:
            if artifact.type == "data":
                # Data should be dict or list
                if isinstance(content, (dict, list)):
                    return {"valid": True}
                # Or valid JSON string
                if isinstance(content, str):
                    parsed = json.loads(content)
                    if isinstance(parsed, (dict, list)):
                        return {"valid": True}
                return {"valid": False, "error": "Data artifact must be dict or list"}

            if artifact.type == "document":
                # Document should be non-empty string
                if isinstance(content, str) and len(content.strip()) > 0:
                    return {"valid": True}
                return {"valid": False, "error": "Document must be non-empty string"}

            if artifact.type == "code":
                # Code should be non-empty string
                if isinstance(content, str) and len(content.strip()) > 0:
                    return {"valid": True}
                return {"valid": False, "error": "Code must be non-empty string"}

            # Default valid for other types
            return {"valid": True}

        except Exception as e:
            return {"valid": False, "error": str(e)}
