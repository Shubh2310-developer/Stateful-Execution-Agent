"""
Cache decorators for automatic caching of function results.

Provides decorators for:
- Automatic caching with TTL
- Cache invalidation
- Freshness checks
"""

import time
from functools import wraps
from typing import Any, Callable, Optional
from datetime import datetime

from src.cache.redis_cache import cache_manager
from src.utils.logger import logger


def cached(
    key_prefix: str,
    key_builder: Optional[Callable] = None,
    ttl: Optional[int] = None,
    include_timestamp: bool = True
):
    """
    Decorator to cache function results.

    Args:
        key_prefix: Prefix for cache keys
        key_builder: Function to build cache key from function args
                    If None, uses first argument as key
        ttl: Time-to-live in seconds
        include_timestamp: Whether to include last_modified timestamp check

    Example:
        @cached(key_prefix="task:state:", key_builder=lambda task_id: task_id)
        async def load_state(task_id: str):
            # ... fetch from database ...
            return state
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Build cache key
            if key_builder:
                cache_key_suffix = key_builder(*args, **kwargs)
            elif args:
                cache_key_suffix = str(args[0])
            else:
                # No key available, skip caching
                logger.warning(
                    f"No cache key available for {func.__name__}, "
                    "executing without cache"
                )
                return await func(*args, **kwargs)

            cache_key = f"{key_prefix}{cache_key_suffix}"

            # Try to get from cache first
            start_time = time.time()
            cached_value = await cache_manager.get(cache_key)

            if cached_value is not None:
                query_time = (time.time() - start_time) * 1000
                logger.debug(
                    f"Cache hit for {func.__name__}: {cache_key} "
                    f"({query_time:.2f}ms)"
                )
                return cached_value

            # Cache miss - execute function
            logger.debug(f"Cache miss for {func.__name__}: {cache_key}")
            start_time = time.time()
            result = await func(*args, **kwargs)
            query_time = (time.time() - start_time) * 1000

            logger.debug(
                f"Query executed for {func.__name__}: {cache_key} "
                f"({query_time:.2f}ms)"
            )

            # Cache the result if not None
            if result is not None:
                # Extract last_modified timestamp if available
                last_modified = None
                if include_timestamp and hasattr(result, 'updated_at'):
                    last_modified = result.updated_at
                elif include_timestamp and isinstance(result, dict):
                    last_modified = result.get('updated_at') or result.get('last_updated')

                await cache_manager.set(
                    cache_key,
                    result,
                    ttl=ttl,
                    last_modified=last_modified
                )

            return result

        return wrapper

    return decorator


def cache_invalidate(
    key_prefix: str,
    key_builder: Optional[Callable] = None,
    pattern: bool = False
):
    """
    Decorator to invalidate cache after function execution.

    Args:
        key_prefix: Prefix for cache keys
        key_builder: Function to build cache key from function args
        pattern: If True, treats key as a pattern and deletes all matching keys

    Example:
        @cache_invalidate(key_prefix="task:state:", key_builder=lambda state: state.task_id)
        async def save_state(state: TaskStateSchema):
            # ... save to database ...
            return success
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Execute the function first
            result = await func(*args, **kwargs)

            # Only invalidate if function succeeded
            if result:
                # Build cache key
                if key_builder:
                    cache_key_suffix = key_builder(*args, **kwargs)
                elif args:
                    # Try to extract from first argument
                    first_arg = args[0]
                    if hasattr(first_arg, 'task_id'):
                        cache_key_suffix = first_arg.task_id
                    elif hasattr(first_arg, 'user_id'):
                        cache_key_suffix = first_arg.user_id
                    else:
                        cache_key_suffix = str(first_arg)
                else:
                    logger.warning(
                        f"No cache key available for invalidation in {func.__name__}"
                    )
                    return result

                cache_key = f"{key_prefix}{cache_key_suffix}"

                if pattern:
                    await cache_manager.delete_pattern(f"{cache_key}*")
                    logger.debug(f"Invalidated cache pattern: {cache_key}*")
                else:
                    await cache_manager.delete(cache_key)
                    logger.debug(f"Invalidated cache: {cache_key}")

            return result

        return wrapper

    return decorator


def cache_with_freshness(
    key_prefix: str,
    key_builder: Optional[Callable] = None,
    ttl: Optional[int] = None,
    freshness_checker: Optional[Callable] = None
):
    """
    Advanced caching decorator with custom freshness checking.

    Args:
        key_prefix: Prefix for cache keys
        key_builder: Function to build cache key from function args
        ttl: Time-to-live in seconds
        freshness_checker: Function that returns (db_last_modified, result)
                          to check if cache is stale

    Example:
        async def check_freshness(task_id):
            # Quick DB query to get just the timestamp
            doc = await db.tasks.find_one({"task_id": task_id}, {"updated_at": 1})
            return doc['updated_at'] if doc else None

        @cache_with_freshness(
            key_prefix="task:state:",
            freshness_checker=check_freshness
        )
        async def load_state(task_id: str):
            # ... fetch full state from database ...
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Build cache key
            if key_builder:
                cache_key_suffix = key_builder(*args, **kwargs)
            elif args:
                cache_key_suffix = str(args[0])
            else:
                return await func(*args, **kwargs)

            cache_key = f"{key_prefix}{cache_key_suffix}"

            # Check freshness if checker is provided
            db_last_modified = None
            if freshness_checker:
                try:
                    db_last_modified = await freshness_checker(*args, **kwargs)
                except Exception as e:
                    logger.warning(
                        f"Freshness check failed for {cache_key}: {str(e)}"
                    )

            # Try to get from cache with freshness check
            cached_value = await cache_manager.get(cache_key, db_last_modified)

            if cached_value is not None:
                logger.debug(f"Fresh cache hit for {func.__name__}: {cache_key}")
                return cached_value

            # Cache miss or stale - execute function
            result = await func(*args, **kwargs)

            # Cache the result
            if result is not None:
                # Use the DB timestamp we already fetched
                last_modified = db_last_modified
                if not last_modified and hasattr(result, 'updated_at'):
                    last_modified = result.updated_at

                await cache_manager.set(
                    cache_key,
                    result,
                    ttl=ttl,
                    last_modified=last_modified
                )

            return result

        return wrapper

    return decorator
