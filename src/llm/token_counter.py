import tiktoken
from typing import Dict, Optional
from src.utils.logger import logger
from src.utils.metrics import MetricsTracker

# Pricing per 1M tokens (approximate for Groq/Llama3 as of Feb 2024)
MODEL_PRICING = {
    "llama3-70b-8192": {"prompt": 0.59, "completion": 0.79},
    "llama3-8b-8192": {"prompt": 0.05, "completion": 0.10},
    "mixtral-8x7b-32768": {"prompt": 0.24, "completion": 0.24},
    "llama-3.3-70b-versatile": {"prompt": 0.59, "completion": 0.79},
    "default": {"prompt": 0.50, "completion": 0.50}
}

class TokenCounter:
    def __init__(self, model_name: str = "llama-3.3-70b-versatile"):
        self.model_name = model_name
        # Using cl100k_base as a standard BPE approximation for many modern LLMs
        try:
            self.encoding = tiktoken.get_encoding("cl100k_base")
        except Exception as e:
            logger.warning(f"Failed to load tiktoken encoding: {e}. Falling back to character count approximation.")
            self.encoding = None

    def count_tokens(self, text: str) -> int:
        if not text:
            return 0
        if not self.encoding:
            return len(text) // 4  # Very rough approximation
        return len(self.encoding.encode(text))

    def count_message_tokens(self, messages: list) -> int:
        num_tokens = 0
        for message in messages:
            num_tokens += 4  # format overhead
            for key, value in message.items():
                num_tokens += self.count_tokens(value)
                if key == "name":
                    num_tokens += -1
        num_tokens += 2  # assistant priming
        return num_tokens

    def calculate_cost(self, prompt_tokens: int, completion_tokens: int, model_name: Optional[str] = None) -> float:
        """Calculates cost in USD based on token counts."""
        model = model_name or self.model_name
        pricing = MODEL_PRICING.get(model, MODEL_PRICING["default"])

        prompt_cost = (prompt_tokens / 1_000_000) * pricing["prompt"]
        completion_cost = (completion_tokens / 1_000_000) * pricing["completion"]

        return prompt_cost + completion_cost

    def report_usage(self, model: str, prompt_tokens: int, completion_tokens: int):
        """Reports usage to the metrics tracker and logs cost."""
        MetricsTracker.track_token_usage(model, "prompt", prompt_tokens)
        MetricsTracker.track_token_usage(model, "completion", completion_tokens)

        cost = self.calculate_cost(prompt_tokens, completion_tokens, model)
        logger.info(f"LLM Usage - Model: {model}, Tokens: {prompt_tokens + completion_tokens}, Estimated Cost: ${cost:.6f}")

token_counter = TokenCounter()
