import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from src.memory.memory_manager import MemoryManager
from src.core.types import UserMemory
from datetime import datetime

@pytest.mark.asyncio
async def test_get_user_memory():
    with patch("src.memory.memory_manager.AsyncIOMotorClient") as mock_client:
        mock_db = mock_client.return_value["test_db"]
        mock_collection = mock_db.memory

        memory_data = {
            "user_id": "u1",
            "profile": {"name": "Test"},
            "preferences": {"tone": "concise"},
            "last_updated": datetime.utcnow()
        }
        mock_collection.find_one = AsyncMock(return_value=memory_data)

        manager = MemoryManager()
        memory = await manager.get_user_memory("u1")

        assert memory.user_id == "u1"
        assert memory.preferences["tone"] == "concise"
        mock_collection.find_one.assert_called_once_with({"user_id": "u1"})

@pytest.mark.asyncio
async def test_save_user_memory():
    with patch("src.memory.memory_manager.AsyncIOMotorClient") as mock_client:
        mock_db = mock_client.return_value["test_db"]
        mock_collection = mock_db.memory
        mock_collection.update_one = AsyncMock(return_value=MagicMock())

        manager = MemoryManager()
        memory = UserMemory(
            user_id="u1",
            profile={"name": "Test"},
            preferences={"tone": "concise"}
        )

        success = await manager.save_user_memory(memory)

        assert success is True
        mock_collection.update_one.assert_called_once()
