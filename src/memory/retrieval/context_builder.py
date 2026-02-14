from typing import Any, Dict, List, Optional, Tuple
from src.core.types import UserMemory, HistoricalPattern
from src.memory.short_term.task_context import TaskContext, StepLog
from src.llm.token_counter import TokenCounter
from src.llm.models.model_config import MODELS, DEFAULT_MODEL
from src.utils.logger import logger

class ContextBuilder:
    """Constructs the comprehensive prompt context from memory and state."""

    def __init__(self, model_name: str = DEFAULT_MODEL):
        self.token_counter = TokenCounter(model_name=model_name)
        self.model_config = MODELS.get(model_name, MODELS["llama-3.3-70b-versatile"])
        self.context_limit = self.model_config["context_window"]
        self.pruning_threshold = 0.8  # 80% of context window

    def build_context(
        self,
        task_context: TaskContext,
        user_memory: Optional[UserMemory] = None,
        relevant_history: List[HistoricalPattern] = None,
        system_prompt: str = ""
    ) -> Dict[str, Any]:
        logger.debug(f"Building context for task {task_context.task_id}")

        # 1. Base Context
        context = {
            "task_id": task_context.task_id,
            "active_step": task_context.active_step,
            "working_variables": task_context.working_variables,
            "recent_notes": task_context.temporary_notes[-5:] if task_context.temporary_notes else []
        }

        # 2. Rank and Prune Historical Patterns (Relevance)
        # Assuming relevant_history is already sorted by relevance (similarity score)
        # If not, we could add sorting here if score was available in HistoricalPattern
        ranked_history = relevant_history or []

        # 3. Step Logs (Recency)
        recent_logs = task_context.step_logs

        # 4. Integrate User Memory
        if user_memory:
            context["user_profile"] = user_memory.profile.dict()
            context["user_preferences"] = user_memory.preferences.dict()

        # 5. Apply Weighted Ranking & Pruning logic
        # For Phase 6.5: weighted ranking balances Relevance (history) with Recency (short-term logs)
        # For now, we will include as much as possible until we hit the threshold

        # Calculate current token usage including system prompt
        current_text = system_prompt + str(context)
        current_tokens = self.token_counter.count_tokens(current_text)

        limit_tokens = int(self.context_limit * self.pruning_threshold)

        # Add Recent Logs (Recency prioritized)
        # Requirements: Keep most recent 3 steps at least
        included_logs = []
        for i, log in enumerate(reversed(recent_logs)):
            log_str = str(log.dict())
            log_tokens = self.token_counter.count_tokens(log_str)

            if i < 3 or (current_tokens + log_tokens < limit_tokens):
                included_logs.insert(0, log.dict())
                current_tokens += log_tokens
            else:
                break

        context["step_logs"] = included_logs

        # Add Historical Experience (Relevance)
        included_history = []
        for hist in ranked_history:
            hist_str = str(hist.dict())
            hist_tokens = self.token_counter.count_tokens(hist_str)

            if current_tokens + hist_tokens < limit_tokens:
                included_history.append(hist.dict())
                current_tokens += hist_tokens
            else:
                break

        context["relevant_past_experiences"] = included_history

        return context
