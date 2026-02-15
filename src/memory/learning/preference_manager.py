from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
from src.core.types import UserPreferences, PreferenceUpdate
from src.utils.logger import logger

class PreferenceManager:
    """
    Manages the identification and persistence of user preferences based on interaction history.

    This component extracts stylistic and behavioral preferences from feedback and
    ensures they are correctly persisted for future task planning.
    """

    def __init__(self, preferences_collection):
        """
        Initializes the PreferenceManager.

        Args:
            preferences_collection: MongoDB collection for user profiles/preferences.
        """
        self.collection = preferences_collection

    async def get_preferences(self, user_id: str) -> Optional[UserPreferences]:
        """
        Retrieves the current preferences for a specific user.

        Args:
            user_id (str): The unique identifier for the user.

        Returns:
            Optional[UserPreferences]: The user's preferences if found, else None.
        """
        user_doc = await self.collection.find_one({"user_id": user_id})
        if user_doc and "preferences" in user_doc:
            return UserPreferences(**user_doc["preferences"])
        return None

    def identify_updates(self, text_feedback: str, rating: int) -> List[PreferenceUpdate]:
        """
        Analyzes feedback to identify potential updates to user preferences.

        Args:
            text_feedback (str): Raw text feedback from the user.
            rating (int): Numeric rating associated with the feedback.

        Returns:
            List[PreferenceUpdate]: A list of identified updates with confidence scores
                and reasoning.
        """
        updates = []
        text_lower = text_feedback.lower()

        # Detail level
        if any(word in text_lower for word in ["shorter", "brief", "concise"]):
            updates.append(PreferenceUpdate(
                field="detail_level", old_value="medium", new_value="concise",
                confidence=0.8, reasoning="User indicated preference for conciseness"
            ))
        elif any(word in text_lower for word in ["more detail", "elaborate", "comprehensive"]):
            updates.append(PreferenceUpdate(
                field="detail_level", old_value="medium", new_value="comprehensive",
                confidence=0.8, reasoning="User requested more detail"
            ))

        # Tone
        if "professional" in text_lower or "formal" in text_lower:
            updates.append(PreferenceUpdate(
                field="document_tone", old_value="casual", new_value="professional",
                confidence=0.7, reasoning="User prefers professional tone"
            ))

        return updates

    async def apply_updates(self, user_id: str, updates: List[PreferenceUpdate]) -> bool:
        """
        Persists a list of preference updates to the user's profile in the database.

        Args:
            user_id (str): The user identifier.
            updates (List[PreferenceUpdate]): The updates to apply.

        Returns:
            bool: True if updates were successfully applied, False otherwise.
        """
        if not updates:
            return True

        set_ops = {"last_updated": datetime.now(timezone.utc)}
        for update in updates:
            set_ops[f"preferences.{update.field}"] = update.new_value

        try:
            await self.collection.update_one(
                {"user_id": user_id},
                {"$set": set_ops},
                upsert=True
            )
            return True
        except Exception as e:
            logger.error(f"Failed to apply preference updates: {e}")
            return False
