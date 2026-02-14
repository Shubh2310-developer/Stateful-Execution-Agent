import logging
from typing import Any, Callable
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log
)
from src.core.exceptions import LLMError
from src.core.constants import MAX_RETRIES
from src.utils.logger import logger

def get_retry_decorator(max_attempts: int = MAX_RETRIES) -> Callable:
    """
    Returns a tenacity retry decorator configured for LLM calls.
    Retries on LLMError with exponential backoff.
    """
    return retry(
        reraise=True,
        stop=stop_after_attempt(max_attempts),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(LLMError),
        before_sleep=before_sleep_log(logger, logging.WARNING)
    )

# Legacy support or alternative name
retry_with_exponential_backoff = get_retry_decorator
