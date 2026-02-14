import json
import re
from typing import Any, Dict, Optional, Type, TypeVar, Tuple
from pydantic import BaseModel, ValidationError
from src.core.exceptions import LLMError
from src.utils.logger import logger

T = TypeVar("T", bound=BaseModel)

class ResponseParser:
    @staticmethod
    def _repair_json(text: str) -> str:
        """Attempts to repair common JSON malformations."""
        # 1. Remove trailing commas before closing braces/brackets
        text = re.sub(r",\s*([\}\]])", r"\1", text)

        # 2. Replace single quotes with double quotes for keys
        text = re.sub(r"\'(\w+)\'\s*:", r'"\1":', text)

        # 3. Replace single quotes with double quotes for string values
        # This is more careful to avoid breaking apostrophes inside already double-quoted strings
        # although this method is only called if initial parsing failed.
        text = re.sub(r":\s*\'(.*?)\'", r': "\1"', text)

        # 4. Handle Python-style Booleans/None if the model outputted them
        text = text.replace(": True", ": true").replace(": False", ": false").replace(": None", ": null")

        return text

    @staticmethod
    def parse_json_response(response_text: str, model_schema: Optional[Type[T]] = None) -> Any:
        """
        Extracts and parses JSON from LLM response text.
        Optionally validates against a Pydantic model.
        """
        try:
            # 1. Attempt to find JSON within markdown blocks first
            json_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", response_text, re.DOTALL)
            if json_match:
                # Use greedy matching for the content inside markdown to handle nested braces
                markdown_content = re.search(r"```(?:json)?\s*(\{.*\})\s*```", response_text, re.DOTALL)
                cleaned_text = markdown_content.group(1) if markdown_content else json_match.group(1)
            else:
                # 2. If no markdown blocks, find the outermost braces
                start_index = response_text.find('{')
                end_index = response_text.rfind('}')

                if start_index != -1 and end_index != -1:
                    cleaned_text = response_text[start_index:end_index + 1]
                else:
                    cleaned_text = response_text.strip()

            cleaned_text = cleaned_text.strip()

            # 4. Parse JSON
            try:
                data = json.loads(cleaned_text)
            except json.JSONDecodeError:
                # 4b. Attempt repair
                logger.warning("Initial JSON parse failed. Attempting repair...")
                repaired_text = ResponseParser._repair_json(cleaned_text)
                data = json.loads(repaired_text)

            # 5. Optional Validation
            if model_schema:
                try:
                    return model_schema.parse_obj(data)
                except ValidationError as ve:
                    logger.error(f"Validation failed for schema {model_schema.__name__}: {str(ve)}")
                    raise LLMError(f"Response did not match expected schema: {str(ve)}")

            return data

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON from LLM response: {response_text}")
            raise LLMError(f"Invalid JSON response from model: {str(e)}")
        except Exception as e:
            if isinstance(e, LLMError):
                raise e
            logger.error(f"Unexpected error parsing LLM response: {str(e)}")
            raise LLMError(f"Failed to process model response: {str(e)}")

    @staticmethod
    def extract_action_and_params(response: Any) -> Tuple[Optional[str], Dict[str, Any]]:
        """Extracts action name and parameters from a tool-use response."""
        # Handle both raw dict and Pydantic model
        if hasattr(response, 'dict'):
            response_dict = response.dict()
        elif isinstance(response, dict):
            response_dict = response
        else:
            return None, {}

        action = response_dict.get("action")
        params = response_dict.get("parameters", {})
        return action, params
