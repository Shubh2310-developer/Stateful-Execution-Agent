"""
Redis Cache Manager with async operations, TTL management, and freshness guarantees.

Provides caching for:
- Task state retrieval
- User memory retrieval
- Task artifacts retrieval

Features:
- Async Redis operations with connection pooling
- TTL-based expiration with configurable timeouts
- JSON serialization for complex objects
- Freshness guarantees (never serve stale data)
- Graceful fallback when Redis is unavailable
- Performance metrics logging
"""

import json
import time
from typing import Any, Dict, Optional, List
from datetime import datetime, timezone
from contextlib import asynccontextmanager

import redis.asyncio as redis
from redis.asyncio.connection import ConnectionPool
from redis.exceptions import RedisError, ConnectionError as RedisConnectionError

from src.core.config import settings
from src.utils.logger import logger


class CacheMetrics:
    """Tracks cache performance metrics."""

    def __init__(self):
        self.hits = 0
        self.misses = 0
        self.errors = 0
        self.total_query_time_with_cache = 0.0
        self.total_query_time_without_cache = 0.0
        self.query_count_with_cache = 0
        self.query_count_without_cache = 0

    def record_hit(self, query_time: float):
        self.hits += 1
        self.total_query_time_with_cache += query_time
        self.query_count_with_cache += 1

    def record_miss(self, query_time: float):
        self.misses += 1
        self.total_query_time_without_cache += query_time
        self.query_count_without_cache += 1

    def record_error(self):
        self.errors += 1

    @property
    def hit_rate(self) -> float:
        total = self.hits + self.misses
        return (self.hits / total * 100) if total > 0 else 0.0

    @property
    def avg_time_with_cache(self) -> float:
        return (self.total_query_time_with_cache / self.query_count_with_cache
                if self.query_count_with_cache > 0 else 0.0)

    @property
    def avg_time_without_cache(self) -> float:
        return (self.total_query_time_without_cache / self.query_count_without_cache
                if self.query_count_without_cache > 0 else 0.0)

    def log_stats(self):
        """Log current cache statistics."""
        logger.info(
            f"Cache Stats: Hit Rate={self.hit_rate:.2f}%, "
            f"Hits={self.hits}, Misses={self.misses}, Errors={self.errors}, "
            f"Avg Time (cached)={self.avg_time_with_cache*1000:.2f}ms, "
            f"Avg Time (uncached)={self.avg_time_without_cache*1000:.2f}ms"
        )


class RedisCacheManager:
    """
    Manages Redis caching operations with connection pooling,
    TTL management, and freshness guarantees.
    """

    # Cache key prefixes for different entity types
    PREFIX_TASK_STATE = "task:state:"
    PREFIX_USER_MEMORY = "user:memory:"
    PREFIX_TASK_ARTIFACTS = "task:artifacts:"

    def __init__(self):
        self.enabled = settings.cache.enabled if hasattr(settings, 'cache') else True
        self.pool: Optional[ConnectionPool] = None
        self.client: Optional[redis.Redis] = None
        self.metrics = CacheMetrics()
        self._initialized = False
        self._last_stats_log = time.time()
        self._stats_log_interval = 300  # Log stats every 5 minutes

    async def initialize(self):
        """Initialize Redis connection pool."""
        if self._initialized:
            return

        if not self.enabled:
            logger.warning("Redis cache is disabled in configuration")
            return

        try:
            # Get Redis URI from settings, with fallback
            redis_uri = getattr(
                getattr(settings, 'cache', None),
                'redis_uri',
                'redis://localhost:6379/0'
            )

            # Create connection pool for better performance
            self.pool = ConnectionPool.from_url(
                redis_uri,
                max_connections=20,
                decode_responses=True,
                socket_timeout=2.0,
                socket_connect_timeout=2.0,
                retry_on_timeout=True
            )

            self.client = redis.Redis(connection_pool=self.pool)

            # Test connection
            await self.client.ping()
            logger.info(f"Redis cache initialized successfully: {redis_uri}")
            self._initialized = True

        except (RedisConnectionError, RedisError) as e:
            logger.error(f"Failed to initialize Redis cache: {str(e)}")
            logger.warning("Application will continue without cache")
            self.enabled = False

    async def close(self):
        """Close Redis connection pool."""
        if self.client:
            await self.client.close()
        if self.pool:
            await self.pool.disconnect()
        logger.info("Redis cache connections closed")

    def _get_ttl(self, entity_type: str) -> int:
        """Get TTL in seconds for a given entity type."""
        cache_config = getattr(settings, 'cache', None)
        if cache_config:
            ttl_config = getattr(cache_config, 'ttl', {})
            return ttl_config.get(entity_type, 300)  # Default 5 minutes
        return 300

    def _serialize_value(self, value: Any, last_modified: Optional[datetime] = None) -> str:
        """
        Serialize value to JSON string with metadata.

        Includes last_modified timestamp for freshness checks.
        """
        cache_entry = {
            "value": value,
            "cached_at": datetime.now(timezone.utc).isoformat(),
            "last_modified": last_modified.isoformat() if last_modified else None
        }
        return json.dumps(cache_entry, default=str)

    def _deserialize_value(self, data: str) -> Dict[str, Any]:
        """Deserialize JSON string to value with metadata."""
        cache_entry = json.loads(data)

        # Parse timestamps back to datetime objects
        if cache_entry.get("cached_at"):
            cache_entry["cached_at"] = datetime.fromisoformat(cache_entry["cached_at"])
        if cache_entry.get("last_modified"):
            cache_entry["last_modified"] = datetime.fromisoformat(cache_entry["last_modified"])

        return cache_entry

    def _check_freshness(
        self,
        cache_entry: Dict[str, Any],
        db_last_modified: Optional[datetime]
    ) -> bool:
        """
        Check if cached data is still fresh compared to database.

        Returns True if cache is fresh (can be used), False if stale.
        """
        if not db_last_modified:
            # If no DB timestamp available, assume cache is valid within TTL
            return True

        cached_last_modified = cache_entry.get("last_modified")
        if not cached_last_modified:
            # No timestamp in cache, consider it stale
            return False

        # Ensure both are timezone-aware for comparison
        if cached_last_modified.tzinfo is None:
            cached_last_modified = cached_last_modified.replace(tzinfo=timezone.utc)
        if db_last_modified.tzinfo is None:
            db_last_modified = db_last_modified.replace(tzinfo=timezone.utc)

        # Cache is fresh if cached version is >= database version
        is_fresh = cached_last_modified >= db_last_modified

        if not is_fresh:
            logger.debug(
                f"Stale cache detected: cached={cached_last_modified}, "
                f"db={db_last_modified}"
            )

        return is_fresh

    async def get(
        self,
        key: str,
        db_last_modified: Optional[datetime] = None
    ) -> Optional[Any]:
        """
        Get value from cache with freshness check.

        Args:
            key: Cache key
            db_last_modified: Last modification timestamp from database
                            (for freshness verification)

        Returns:
            Cached value if fresh, None if not found or stale
        """
        if not self.enabled or not self._initialized:
            return None

        start_time = time.time()

        try:
            data = await self.client.get(key)
            query_time = time.time() - start_time

            if data is None:
                self.metrics.record_miss(query_time)
                self._log_stats_if_needed()
                return None

            cache_entry = self._deserialize_value(data)

            # Check freshness if database timestamp is provided
            if db_last_modified and not self._check_freshness(cache_entry, db_last_modified):
                logger.debug(f"Cache stale for key: {key}")
                await self.delete(key)  # Remove stale data
                self.metrics.record_miss(query_time)
                self._log_stats_if_needed()
                return None

            self.metrics.record_hit(query_time)
            self._log_stats_if_needed()
            logger.debug(f"Cache HIT: {key} ({query_time*1000:.2f}ms)")

            return cache_entry["value"]

        except (RedisError, json.JSONDecodeError) as e:
            logger.warning(f"Cache get error for key {key}: {str(e)}")
            self.metrics.record_error()
            return None

    async def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None,
        last_modified: Optional[datetime] = None
    ) -> bool:
        """
        Set value in cache with TTL.

        Args:
            key: Cache key
            value: Value to cache (will be JSON serialized)
            ttl: Time-to-live in seconds (uses default if None)
            last_modified: Last modification timestamp for freshness tracking

        Returns:
            True if successful, False otherwise
        """
        if not self.enabled or not self._initialized:
            return False

        try:
            # Extract TTL from key prefix if not provided
            if ttl is None:
                if key.startswith(self.PREFIX_TASK_STATE):
                    ttl = self._get_ttl("task_state")
                elif key.startswith(self.PREFIX_USER_MEMORY):
                    ttl = self._get_ttl("user_memory")
                elif key.startswith(self.PREFIX_TASK_ARTIFACTS):
                    ttl = self._get_ttl("task_artifacts")
                else:
                    ttl = 300  # Default 5 minutes

            serialized = self._serialize_value(value, last_modified)
            await self.client.setex(key, ttl, serialized)

            logger.debug(f"Cache SET: {key} (TTL={ttl}s)")
            return True

        except (RedisError, TypeError) as e:
            logger.warning(f"Cache set error for key {key}: {str(e)}")
            self.metrics.record_error()
            return False

    async def delete(self, key: str) -> bool:
        """
        Delete value from cache.

        Args:
            key: Cache key to delete

        Returns:
            True if successful, False otherwise
        """
        if not self.enabled or not self._initialized:
            return False

        try:
            await self.client.delete(key)
            logger.debug(f"Cache DELETE: {key}")
            return True
        except RedisError as e:
            logger.warning(f"Cache delete error for key {key}: {str(e)}")
            self.metrics.record_error()
            return False

    async def delete_pattern(self, pattern: str) -> int:
        """
        Delete all keys matching a pattern.

        Args:
            pattern: Redis key pattern (e.g., "task:artifacts:*")

        Returns:
            Number of keys deleted
        """
        if not self.enabled or not self._initialized:
            return 0

        try:
            keys = []
            async for key in self.client.scan_iter(match=pattern, count=100):
                keys.append(key)

            if keys:
                deleted = await self.client.delete(*keys)
                logger.debug(f"Cache DELETE pattern: {pattern} ({deleted} keys)")
                return deleted
            return 0

        except RedisError as e:
            logger.warning(f"Cache delete pattern error for {pattern}: {str(e)}")
            self.metrics.record_error()
            return 0

    async def invalidate_task(self, task_id: str):
        """
        Invalidate all cache entries related to a task.

        Called when task state or artifacts are updated.
        """
        await self.delete(f"{self.PREFIX_TASK_STATE}{task_id}")
        await self.delete_pattern(f"{self.PREFIX_TASK_ARTIFACTS}{task_id}")
        logger.debug(f"Invalidated cache for task: {task_id}")

    async def invalidate_user_memory(self, user_id: str):
        """
        Invalidate cache entries for user memory.

        Called when user memory or preferences are updated.
        """
        await self.delete(f"{self.PREFIX_USER_MEMORY}{user_id}")
        logger.debug(f"Invalidated cache for user memory: {user_id}")

    def _log_stats_if_needed(self):
        """Log cache statistics periodically."""
        current_time = time.time()
        if current_time - self._last_stats_log >= self._stats_log_interval:
            self.metrics.log_stats()
            self._last_stats_log = current_time

    async def get_cache_info(self) -> Dict[str, Any]:
        """
        Get cache information and statistics.

        Returns:
            Dictionary with cache metrics and Redis info
        """
        info = {
            "enabled": self.enabled,
            "initialized": self._initialized,
            "metrics": {
                "hit_rate": self.metrics.hit_rate,
                "hits": self.metrics.hits,
                "misses": self.metrics.misses,
                "errors": self.metrics.errors,
                "avg_time_cached_ms": self.metrics.avg_time_with_cache * 1000,
                "avg_time_uncached_ms": self.metrics.avg_time_without_cache * 1000
            }
        }

        if self._initialized and self.client:
            try:
                redis_info = await self.client.info("stats")
                info["redis"] = {
                    "total_connections_received": redis_info.get("total_connections_received"),
                    "total_commands_processed": redis_info.get("total_commands_processed"),
                    "keyspace_hits": redis_info.get("keyspace_hits"),
                    "keyspace_misses": redis_info.get("keyspace_misses")
                }
            except RedisError:
                pass

        return info


# Global cache manager instance
cache_manager = RedisCacheManager()
