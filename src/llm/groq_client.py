from typing import List, Dict, Any, Optional, AsyncGenerator
import os
from groq import AsyncGroq
from src.core.config import settings
from src.core.exceptions import LLMError
from src.utils.logger import logger
from src.llm.retry_handler import get_retry_decorator
from src.llm.token_counter import token_counter

class GroqClient:
    def __init__(self, api_key: Optional[str] = None):
        self._api_key = api_key or settings.llm.api_key
        self._client: Optional[AsyncGroq] = None
        self.model = settings.llm.model

    @property
    def client(self) -> AsyncGroq:
        if self._client is None:
            if not self._api_key:
                logger.error("Groq API key is not configured.")
                raise LLMError("Groq API key is not configured.")
            try:
                self._client = AsyncGroq(api_key=self._api_key)
            except Exception as e:
                logger.error(f"Failed to initialize Groq client: {e}")
                raise LLMError(f"Failed to initialize Groq client: {e}")
        return self._client

    @get_retry_decorator()
    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 4096,
        response_format: Optional[Dict[str, str]] = None,
        stream: bool = False
    ) -> Any:
        """
        Generates a response from the Groq API asynchronously with retries and token tracking.
        Supports both streaming and non-streaming responses.
        """
        if stream:
            return self._stream_response(messages, temperature, max_tokens, response_format)

        try:
            # Track input tokens
            input_tokens = token_counter.count_message_tokens(messages)
            logger.debug(f"Input tokens: {input_tokens}")

            logger.debug(f"Sending request to Groq model: {self.model}")

            completion = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                response_format=response_format,
                stream=False
            )

            response_content = completion.choices[0].message.content

            # Track output tokens
            output_tokens = token_counter.count_tokens(response_content)
            logger.debug(f"Output tokens: {output_tokens}")

            # Log total usage if usage info is provided by the API
            if hasattr(completion, 'usage'):
                token_counter.report_usage(
                    model=self.model,
                    prompt_tokens=completion.usage.prompt_tokens,
                    completion_tokens=completion.usage.completion_tokens
                )

            return response_content

        except Exception as e:
            if isinstance(e, LLMError):
                raise e
            logger.error(f"Error calling Groq API: {str(e)}")
            raise LLMError(f"Failed to generate response from Groq: {str(e)}")

    async def _stream_response(
        self,
        messages: List[Dict[str, str]],
        temperature: float,
        max_tokens: int,
        response_format: Optional[Dict[str, str]]
    ) -> AsyncGenerator[str, None]:
        """Internal generator for streaming responses."""
        response_content = []
        try:
            stream = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                response_format=response_format,
                stream=True
            )

            async for chunk in stream:
                content = chunk.choices[0].delta.content
                if content:
                    response_content.append(content)
                    yield content

            # Final token tracking for the whole stream
            full_content = "".join(response_content)
            output_tokens = token_counter.count_tokens(full_content)
            # Log approximate usage for stream
            input_tokens = token_counter.count_message_tokens(messages)
            token_counter.report_usage(
                model=self.model,
                prompt_tokens=input_tokens,
                completion_tokens=output_tokens
            )

        except Exception as e:
            logger.error(f"Error in Groq stream: {str(e)}")
            raise LLMError(f"Stream interrupted: {str(e)}")

# Global instance
groq_client = GroqClient()
