"""
Unit tests for Redis cache implementation.

Tests cache operations, TTL management, freshness checks, and invalidation logic.
"""

import pytest
from datetime import datetime, timezone, timedelta
from unittest.mock import AsyncMock, MagicMock, patch

from src.cache.redis_cache import RedisCacheManager, CacheMetrics
from src.core.config import settings


@pytest.fixture
def mock_redis_client():
    """Mock Redis client for testing."""
    client = AsyncMock()
    client.ping = AsyncMock(return_value=True)
    client.get = AsyncMock(return_value=None)
    client.setex = AsyncMock(return_value=True)
    client.delete = AsyncMock(return_value=1)
    client.scan_iter = AsyncMock(return_value=[])
    client.close = AsyncMock()
    client.info = AsyncMock(return_value={
        "total_connections_received": 100,
        "total_commands_processed": 1000,
        "keyspace_hits": 750,
        "keyspace_misses": 250
    })
    return client


@pytest.fixture
def cache_manager_with_mock(mock_redis_client):
    """Cache manager with mocked Redis client."""
    manager = RedisCacheManager()
    manager.client = mock_redis_client
    manager._initialized = True
    manager.enabled = True
    return manager


class TestCacheMetrics:
    """Test cache metrics tracking."""

    def test_initial_metrics(self):
        metrics = CacheMetrics()
        assert metrics.hits == 0
        assert metrics.misses == 0
        assert metrics.errors == 0
        assert metrics.hit_rate == 0.0

    def test_record_hit(self):
        metrics = CacheMetrics()
        metrics.record_hit(0.001)
        assert metrics.hits == 1
        assert metrics.query_count_with_cache == 1

    def test_record_miss(self):
        metrics = CacheMetrics()
        metrics.record_miss(0.005)
        assert metrics.misses == 1
        assert metrics.query_count_without_cache == 1

    def test_hit_rate_calculation(self):
        metrics = CacheMetrics()
        metrics.record_hit(0.001)
        metrics.record_hit(0.001)
        metrics.record_hit(0.001)
        metrics.record_miss(0.005)
        assert metrics.hit_rate == 75.0  # 3 hits out of 4 total

    def test_average_times(self):
        metrics = CacheMetrics()
        metrics.record_hit(0.001)
        metrics.record_hit(0.002)
        metrics.record_miss(0.010)
        assert metrics.avg_time_with_cache == 0.0015
        assert metrics.avg_time_without_cache == 0.010


class TestRedisCacheManager:
    """Test Redis cache manager operations."""

    @pytest.mark.asyncio
    async def test_initialize_success(self, mock_redis_client):
        """Test successful cache initialization."""
        with patch('src.cache.redis_cache.redis.Redis') as mock_redis_class, \
             patch('src.cache.redis_cache.ConnectionPool.from_url') as mock_pool:

            mock_redis_class.return_value = mock_redis_client
            mock_pool.return_value = MagicMock()

            manager = RedisCacheManager()
            await manager.initialize()

            assert manager._initialized is True
            assert manager.enabled is True
            mock_redis_client.ping.assert_called_once()

    @pytest.mark.asyncio
    async def test_initialize_failure_graceful(self):
        """Test graceful handling of initialization failure."""
        with patch('src.cache.redis_cache.ConnectionPool.from_url') as mock_pool:
            mock_pool.side_effect = Exception("Connection failed")

            manager = RedisCacheManager()
            await manager.initialize()

            assert manager._initialized is False
            assert manager.enabled is False

    @pytest.mark.asyncio
    async def test_serialize_deserialize_value(self, cache_manager_with_mock):
        """Test value serialization and deserialization."""
        manager = cache_manager_with_mock

        test_data = {"task_id": "test-123", "status": "COMPLETED"}
        last_modified = datetime.now(timezone.utc)

        serialized = manager._serialize_value(test_data, last_modified)
        assert isinstance(serialized, str)

        deserialized = manager._deserialize_value(serialized)
        assert deserialized["value"] == test_data
        assert isinstance(deserialized["cached_at"], datetime)
        assert isinstance(deserialized["last_modified"], datetime)

    @pytest.mark.asyncio
    async def test_check_freshness_valid(self, cache_manager_with_mock):
        """Test freshness check with valid cache."""
        manager = cache_manager_with_mock

        now = datetime.now(timezone.utc)
        cache_entry = {
            "value": {"test": "data"},
            "cached_at": now,
            "last_modified": now
        }

        db_last_modified = now - timedelta(seconds=10)
        is_fresh = manager._check_freshness(cache_entry, db_last_modified)
        assert is_fresh is True

    @pytest.mark.asyncio
    async def test_check_freshness_stale(self, cache_manager_with_mock):
        """Test freshness check with stale cache."""
        manager = cache_manager_with_mock

        old_time = datetime.now(timezone.utc) - timedelta(minutes=5)
        new_time = datetime.now(timezone.utc)

        cache_entry = {
            "value": {"test": "data"},
            "cached_at": old_time,
            "last_modified": old_time
        }

        is_fresh = manager._check_freshness(cache_entry, new_time)
        assert is_fresh is False

    @pytest.mark.asyncio
    async def test_get_cache_hit(self, cache_manager_with_mock, mock_redis_client):
        """Test cache get with hit."""
        manager = cache_manager_with_mock

        test_data = {"task_id": "test-123"}
        serialized = manager._serialize_value(test_data)
        mock_redis_client.get.return_value = serialized

        result = await manager.get("test:key")

        assert result == test_data
        assert manager.metrics.hits == 1
        mock_redis_client.get.assert_called_once_with("test:key")

    @pytest.mark.asyncio
    async def test_get_cache_miss(self, cache_manager_with_mock, mock_redis_client):
        """Test cache get with miss."""
        manager = cache_manager_with_mock
        mock_redis_client.get.return_value = None

        result = await manager.get("test:key")

        assert result is None
        assert manager.metrics.misses == 1

    @pytest.mark.asyncio
    async def test_get_with_stale_data(self, cache_manager_with_mock, mock_redis_client):
        """Test cache get with stale data detection."""
        manager = cache_manager_with_mock

        old_time = datetime.now(timezone.utc) - timedelta(minutes=5)
        test_data = {"task_id": "test-123"}
        serialized = manager._serialize_value(test_data, old_time)
        mock_redis_client.get.return_value = serialized

        db_last_modified = datetime.now(timezone.utc)
        result = await manager.get("test:key", db_last_modified)

        assert result is None
        assert manager.metrics.misses == 1
        # Verify stale cache was deleted
        mock_redis_client.delete.assert_called_once_with("test:key")

    @pytest.mark.asyncio
    async def test_set_cache(self, cache_manager_with_mock, mock_redis_client):
        """Test cache set operation."""
        manager = cache_manager_with_mock

        test_data = {"task_id": "test-123"}
        last_modified = datetime.now(timezone.utc)

        result = await manager.set("test:key", test_data, ttl=300, last_modified=last_modified)

        assert result is True
        mock_redis_client.setex.assert_called_once()
        call_args = mock_redis_client.setex.call_args
        assert call_args[0][0] == "test:key"
        assert call_args[0][1] == 300

    @pytest.mark.asyncio
    async def test_set_cache_with_prefix_ttl(self, cache_manager_with_mock, mock_redis_client):
        """Test cache set with TTL determined by key prefix."""
        manager = cache_manager_with_mock

        test_data = {"task_id": "test-123"}
        key = f"{manager.PREFIX_TASK_STATE}test-123"

        result = await manager.set(key, test_data)

        assert result is True
        mock_redis_client.setex.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_cache(self, cache_manager_with_mock, mock_redis_client):
        """Test cache delete operation."""
        manager = cache_manager_with_mock

        result = await manager.delete("test:key")

        assert result is True
        mock_redis_client.delete.assert_called_once_with("test:key")

    @pytest.mark.asyncio
    async def test_delete_pattern(self, cache_manager_with_mock, mock_redis_client):
        """Test cache delete with pattern matching."""
        manager = cache_manager_with_mock

        async def mock_scan_iter(match, count):
            for key in ["task:123:a", "task:123:b"]:
                yield key

        mock_redis_client.scan_iter = mock_scan_iter
        mock_redis_client.delete.return_value = 2

        result = await manager.delete_pattern("task:123:*")

        assert result == 2

    @pytest.mark.asyncio
    async def test_invalidate_task(self, cache_manager_with_mock, mock_redis_client):
        """Test task cache invalidation."""
        manager = cache_manager_with_mock

        async def mock_scan_iter(match, count):
            return []

        mock_redis_client.scan_iter = mock_scan_iter

        await manager.invalidate_task("task-123")

        # Should delete state and artifacts
        assert mock_redis_client.delete.call_count >= 1

    @pytest.mark.asyncio
    async def test_invalidate_user_memory(self, cache_manager_with_mock, mock_redis_client):
        """Test user memory cache invalidation."""
        manager = cache_manager_with_mock

        await manager.invalidate_user_memory("user-456")

        mock_redis_client.delete.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_cache_info(self, cache_manager_with_mock):
        """Test cache info retrieval."""
        manager = cache_manager_with_mock
        manager.metrics.record_hit(0.001)
        manager.metrics.record_hit(0.002)
        manager.metrics.record_miss(0.010)

        info = await manager.get_cache_info()

        assert info["enabled"] is True
        assert info["initialized"] is True
        assert "metrics" in info
        assert info["metrics"]["hit_rate"] > 0
        assert "redis" in info

    @pytest.mark.asyncio
    async def test_graceful_fallback_when_disabled(self):
        """Test that cache operations gracefully handle disabled state."""
        manager = RedisCacheManager()
        manager.enabled = False

        result = await manager.get("test:key")
        assert result is None

        result = await manager.set("test:key", {"data": "test"})
        assert result is False

        result = await manager.delete("test:key")
        assert result is False


class TestCacheErrorHandling:
    """Test cache error handling and resilience."""

    @pytest.mark.asyncio
    async def test_get_handles_redis_error(self, cache_manager_with_mock, mock_redis_client):
        """Test that get handles Redis errors gracefully."""
        manager = cache_manager_with_mock
        mock_redis_client.get.side_effect = Exception("Redis connection error")

        result = await manager.get("test:key")

        assert result is None
        assert manager.metrics.errors == 1

    @pytest.mark.asyncio
    async def test_set_handles_redis_error(self, cache_manager_with_mock, mock_redis_client):
        """Test that set handles Redis errors gracefully."""
        manager = cache_manager_with_mock
        mock_redis_client.setex.side_effect = Exception("Redis connection error")

        result = await manager.set("test:key", {"data": "test"})

        assert result is False
        assert manager.metrics.errors == 1

    @pytest.mark.asyncio
    async def test_delete_handles_redis_error(self, cache_manager_with_mock, mock_redis_client):
        """Test that delete handles Redis errors gracefully."""
        manager = cache_manager_with_mock
        mock_redis_client.delete.side_effect = Exception("Redis connection error")

        result = await manager.delete("test:key")

        assert result is False
        assert manager.metrics.errors == 1
