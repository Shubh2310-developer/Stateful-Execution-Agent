"""
Integration tests for Redis caching with database operations.

Tests the complete caching flow with real database adapter interactions.
"""

import pytest
from datetime import datetime, timezone
from unittest.mock import AsyncMock, patch, MagicMock

from src.state.persistence.database_adapter import DatabaseAdapter
from src.cache.redis_cache import cache_manager
from src.state.state_schema import TaskStateSchema
from src.core.types import Goal, TaskStatus, Artifact
from src.memory.memory_manager import MemoryManager
from src.core.types import UserMemory, UserProfile, UserPreferences


@pytest.fixture
async def mock_cache_manager():
    """Mock cache manager for testing."""
    manager = MagicMock()
    manager.get = AsyncMock(return_value=None)
    manager.set = AsyncMock(return_value=True)
    manager.delete = AsyncMock(return_value=True)
    manager.delete_pattern = AsyncMock(return_value=1)
    manager.invalidate_task = AsyncMock()
    manager.invalidate_user_memory = AsyncMock()
    manager.PREFIX_TASK_STATE = "task:state:"
    manager.PREFIX_USER_MEMORY = "user:memory:"
    manager.PREFIX_TASK_ARTIFACTS = "task:artifacts:"
    return manager


@pytest.fixture
async def mock_db_adapter():
    """Mock database adapter."""
    adapter = MagicMock()
    adapter.tasks = MagicMock()
    adapter.tasks.find_one = AsyncMock(return_value=None)
    adapter.tasks.find_one_and_update = AsyncMock(return_value={"version_counter": 2})
    adapter.artifacts = MagicMock()
    adapter.artifacts.find = MagicMock()
    adapter.artifacts.update_one = AsyncMock()
    return adapter


class TestDatabaseAdapterCaching:
    """Test caching integration with DatabaseAdapter."""

    @pytest.mark.asyncio
    async def test_load_state_cache_miss_then_cache(self, mock_db_adapter, mock_cache_manager):
        """Test load_state with cache miss, then caches result."""
        with patch('src.state.persistence.database_adapter.cache_manager', mock_cache_manager):
            adapter = DatabaseAdapter()
            adapter.tasks = mock_db_adapter.tasks

            # Mock database response
            db_doc = {
                "task_id": "test-task-123",
                "user_id": "user-1",
                "version_counter": 1,
                "goal": {"request": "test", "success_criteria": [], "constraints": []},
                "status": "PENDING",
                "current_step_index": 0,
                "artifacts": [],
                "decisions": [],
                "metadata": {},
                "updated_at": datetime.now(timezone.utc),
                "created_at": datetime.now(timezone.utc)
            }
            mock_db_adapter.tasks.find_one.return_value = db_doc

            # First call - cache miss
            mock_cache_manager.get.return_value = None
            state = await adapter.load_state("test-task-123")

            assert state is not None
            assert state.task_id == "test-task-123"

            # Verify cache was checked
            mock_cache_manager.get.assert_called_once()

            # Verify result was cached
            mock_cache_manager.set.assert_called_once()

    @pytest.mark.asyncio
    async def test_load_state_cache_hit(self, mock_db_adapter, mock_cache_manager):
        """Test load_state with cache hit (no DB query)."""
        with patch('src.state.persistence.database_adapter.cache_manager', mock_cache_manager):
            adapter = DatabaseAdapter()
            adapter.tasks = mock_db_adapter.tasks

            # Mock cached data
            cached_data = {
                "task_id": "test-task-123",
                "user_id": "user-1",
                "version_counter": 1,
                "goal": {"request": "test", "success_criteria": [], "constraints": []},
                "status": "PENDING",
                "current_step_index": 0,
                "artifacts": [],
                "decisions": [],
                "metadata": {},
                "updated_at": datetime.now(timezone.utc),
                "created_at": datetime.now(timezone.utc)
            }
            mock_cache_manager.get.return_value = cached_data

            state = await adapter.load_state("test-task-123")

            assert state is not None
            assert state.task_id == "test-task-123"

            # Verify DB was NOT queried
            mock_db_adapter.tasks.find_one.assert_not_called()

    @pytest.mark.asyncio
    async def test_save_state_invalidates_cache(self, mock_db_adapter, mock_cache_manager):
        """Test that save_state invalidates task cache."""
        with patch('src.state.persistence.database_adapter.cache_manager', mock_cache_manager):
            adapter = DatabaseAdapter()
            adapter.tasks = mock_db_adapter.tasks
            adapter.versions = MagicMock()
            adapter.versions.insert_one = AsyncMock()
            adapter.client = MagicMock()
            adapter.client.start_session = MagicMock()

            # Create test state
            state = TaskStateSchema(
                task_id="test-task-123",
                user_id="user-1",
                goal=Goal(request="test", success_criteria=[]),
                status=TaskStatus.PENDING,
                version_counter=1
            )

            # Mock transaction not supported to trigger sequential save
            await adapter._save_state_sequential(state, is_milestone=False, summary=None)

            # Verify cache was invalidated
            mock_cache_manager.invalidate_task.assert_called_once_with("test-task-123")

    @pytest.mark.asyncio
    async def test_get_artifacts_cache_miss_then_cache(self, mock_db_adapter, mock_cache_manager):
        """Test get_artifacts with cache miss, then caches result."""
        with patch('src.state.persistence.database_adapter.cache_manager', mock_cache_manager):
            adapter = DatabaseAdapter()
            adapter.artifacts = mock_db_adapter.artifacts

            # Mock cursor
            mock_cursor = MagicMock()
            mock_cursor.to_list = AsyncMock(return_value=[
                {
                    "id": "art-1",
                    "task_id": "test-task-123",
                    "uri": "file://test",
                    "type": "code",
                    "created_at": datetime.now(timezone.utc)
                }
            ])
            mock_db_adapter.artifacts.find.return_value = mock_cursor

            # Cache miss
            mock_cache_manager.get.return_value = None

            artifacts = await adapter.get_artifacts("test-task-123")

            assert len(artifacts) == 1
            assert artifacts[0].id == "art-1"

            # Verify cache was checked and set
            mock_cache_manager.get.assert_called_once()
            mock_cache_manager.set.assert_called_once()

    @pytest.mark.asyncio
    async def test_register_artifact_invalidates_cache(self, mock_db_adapter, mock_cache_manager):
        """Test that register_artifact invalidates artifacts cache."""
        with patch('src.state.persistence.database_adapter.cache_manager', mock_cache_manager):
            adapter = DatabaseAdapter()
            adapter.artifacts = mock_db_adapter.artifacts

            artifact = Artifact(
                id="art-1",
                task_id="test-task-123",
                uri="file://test",
                type="code"
            )

            await adapter.register_artifact(artifact)

            # Verify cache was invalidated
            mock_cache_manager.delete.assert_called_once()
            call_args = mock_cache_manager.delete.call_args[0][0]
            assert "test-task-123" in call_args


class TestMemoryManagerCaching:
    """Test caching integration with MemoryManager."""

    @pytest.mark.asyncio
    async def test_get_user_memory_cache_miss(self, mock_cache_manager):
        """Test get_user_memory with cache miss."""
        with patch('src.memory.memory_manager.cache_manager', mock_cache_manager):
            manager = MemoryManager()
            manager.profiles = MagicMock()
            manager.profiles.find_one = AsyncMock(return_value={
                "user_id": "user-1",
                "profile": {
                    "user_id": "user-1",
                    "role": "developer",
                    "communication_style": "technical",
                    "technical_depth": "high",
                    "last_updated": datetime.now(timezone.utc)
                },
                "preferences": {
                    "document_tone": "technical",
                    "detail_level": "high",
                    "preferred_formats": ["markdown"],
                    "formatting_rules": {}
                },
                "domain_knowledge": {},
                "last_updated": datetime.now(timezone.utc)
            })

            # Cache miss
            mock_cache_manager.get.return_value = None

            memory = await manager.get_user_memory("user-1")

            assert memory is not None
            assert memory.user_id == "user-1"

            # Verify cache was checked and set
            mock_cache_manager.get.assert_called_once()
            mock_cache_manager.set.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_user_memory_cache_hit(self, mock_cache_manager):
        """Test get_user_memory with cache hit."""
        with patch('src.memory.memory_manager.cache_manager', mock_cache_manager):
            manager = MemoryManager()
            manager.profiles = MagicMock()

            # Cache hit
            cached_data = {
                "user_id": "user-1",
                "profile": {
                    "user_id": "user-1",
                    "role": "developer",
                    "communication_style": "technical",
                    "technical_depth": "high",
                    "last_updated": datetime.now(timezone.utc)
                },
                "preferences": {
                    "document_tone": "technical",
                    "detail_level": "high",
                    "preferred_formats": ["markdown"],
                    "formatting_rules": {}
                },
                "domain_knowledge": {},
                "last_updated": datetime.now(timezone.utc)
            }
            mock_cache_manager.get.return_value = cached_data

            memory = await manager.get_user_memory("user-1")

            assert memory is not None
            assert memory.user_id == "user-1"

            # Verify DB was NOT queried
            manager.profiles.find_one.assert_not_called()

    @pytest.mark.asyncio
    async def test_save_user_memory_invalidates_cache(self, mock_cache_manager):
        """Test that save_user_memory invalidates cache."""
        with patch('src.memory.memory_manager.cache_manager', mock_cache_manager):
            manager = MemoryManager()
            manager.profiles = MagicMock()
            manager.profiles.update_one = AsyncMock()

            memory = UserMemory(
                user_id="user-1",
                profile=UserProfile(user_id="user-1"),
                preferences=UserPreferences()
            )

            await manager.save_user_memory(memory)

            # Verify cache was invalidated
            mock_cache_manager.invalidate_user_memory.assert_called_once_with("user-1")

    @pytest.mark.asyncio
    async def test_update_user_preferences_invalidates_cache(self, mock_cache_manager):
        """Test that update_user_preferences invalidates cache."""
        with patch('src.memory.memory_manager.cache_manager', mock_cache_manager):
            manager = MemoryManager()
            manager.profiles = MagicMock()
            manager.profiles.update_one = AsyncMock()

            await manager.update_user_preferences("user-1", {"document_tone": "casual"})

            # Verify cache was invalidated
            mock_cache_manager.invalidate_user_memory.assert_called_once_with("user-1")


class TestCachePerformance:
    """Test cache performance improvements."""

    @pytest.mark.asyncio
    async def test_cache_reduces_query_time(self, mock_db_adapter, mock_cache_manager):
        """Test that cache significantly reduces query time."""
        with patch('src.state.persistence.database_adapter.cache_manager', mock_cache_manager):
            adapter = DatabaseAdapter()
            adapter.tasks = mock_db_adapter.tasks

            # First query - simulate slow DB
            import asyncio

            async def slow_db_query(*args, **kwargs):
                await asyncio.sleep(0.1)  # Simulate 100ms DB query
                return {
                    "task_id": "test-task-123",
                    "user_id": "user-1",
                    "version_counter": 1,
                    "goal": {"request": "test", "success_criteria": [], "constraints": []},
                    "status": "PENDING",
                    "current_step_index": 0,
                    "artifacts": [],
                    "decisions": [],
                    "metadata": {},
                    "updated_at": datetime.now(timezone.utc),
                    "created_at": datetime.now(timezone.utc)
                }

            mock_db_adapter.tasks.find_one = slow_db_query
            mock_cache_manager.get.return_value = None

            import time
            start = time.time()
            await adapter.load_state("test-task-123")
            db_time = time.time() - start

            # Second query - from cache (fast)
            cached_data = {
                "task_id": "test-task-123",
                "user_id": "user-1",
                "version_counter": 1,
                "goal": {"request": "test", "success_criteria": [], "constraints": []},
                "status": "PENDING",
                "current_step_index": 0,
                "artifacts": [],
                "decisions": [],
                "metadata": {},
                "updated_at": datetime.now(timezone.utc),
                "created_at": datetime.now(timezone.utc)
            }
            mock_cache_manager.get.return_value = cached_data

            start = time.time()
            await adapter.load_state("test-task-123")
            cache_time = time.time() - start

            # Cache should be significantly faster
            assert cache_time < db_time / 10  # At least 10x faster
