from typing import List, Dict, Any, Optional
from src.core.types import UserMemory
from src.memory.retrieval.semantic_search import SemanticSearch
from src.memory.retrieval.relevance_ranker import RelevanceRanker
from src.llm.token_counter import token_counter
from src.utils.logger import logger

class AdaptivePlanner:
    """
    Connects the planning process with long-term memory to enable learning from past executions.
    Implements Phase 4.5: Adaptive Planning Integration.
    """

    def __init__(self):
        self.semantic_search = SemanticSearch()
        self.ranker = RelevanceRanker()

    async def prepare_adaptive_context(
        self,
        goal_text: str,
        user_memory: Optional[UserMemory],
        max_lessons: int = 5,
        max_tokens_limit: int = 1500
    ) -> Dict[str, Any]:
        """
        Retrieves, ranks, and formats past experiences and preferences for prompt injection.
        """
        if not user_memory:
            logger.debug("No user memory provided for adaptive planning context.")
            return {
                "lessons_learned": [],
                "user_preferences": {}
            }

        logger.info(f"Preparing adaptive context for goal: {goal_text[:50]}...")

        # 1. Memory Retrieval: Query for similar past goals/patterns
        relevant_patterns = await self.semantic_search.find_relevant_patterns(
            query=goal_text,
            user_id=user_memory.user_id,
            limit=10
        )

        # 2. Context Window Management: Rank and Prune
        # Convert Pydantic models to dicts for the ranker
        pattern_dicts = [p.dict() if hasattr(p, 'dict') else p for p in relevant_patterns]
        ranked_patterns = self.ranker.rank_results(goal_text, pattern_dicts)

        # 3. Context Injection: Format and Token-aware Pruning
        lessons_learned = []
        current_tokens = 0

        for p in ranked_patterns:
            if len(lessons_learned) >= max_lessons:
                break

            task_type = p.get("task_type", "Unknown task")
            approach = p.get("approach", "N/A")
            feedback = p.get("feedback", "")

            lesson = f"Past Task: {task_type} | Strategy: {approach}"
            if feedback:
                lesson += f" | Outcome: {feedback}"

            # Check token budget
            lesson_tokens = token_counter.count_tokens(lesson)
            if current_tokens + lesson_tokens > max_tokens_limit:
                logger.debug(f"Reached token limit ({max_tokens_limit}), skipping further lessons.")
                break

            lessons_learned.append(lesson)
            current_tokens += lesson_tokens

        logger.debug(f"Retrieved {len(lessons_learned)} relevant lessons ({current_tokens} tokens) from memory.")

        return {
            "lessons_learned": lessons_learned,
            "user_preferences": user_memory.preferences
        }
