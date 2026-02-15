#!/usr/bin/env python3
"""
Cache Performance Demo

Demonstrates the performance improvement from Redis caching.
Run this script after starting the application with Redis enabled.
"""

import asyncio
import time
from datetime import datetime
from typing import List, Tuple

from src.cache.redis_cache import cache_manager
from src.state.persistence.database_adapter import DatabaseAdapter
from src.memory.memory_manager import MemoryManager
from src.state.state_schema import TaskStateSchema
from src.core.types import Goal, TaskStatus, UserMemory, UserProfile, UserPreferences
from src.utils.logger import logger


async def benchmark_task_state_caching():
    """Benchmark task state retrieval with and without caching."""
    print("\n" + "="*60)
    print("BENCHMARK: Task State Retrieval")
    print("="*60)

    # Initialize
    await cache_manager.initialize()
    db = DatabaseAdapter()

    # Create a test task
    test_task_id = f"benchmark-task-{int(time.time())}"
    state = TaskStateSchema(
        task_id=test_task_id,
        user_id="benchmark-user",
        goal=Goal(request="Benchmark test", success_criteria=["Complete"]),
        status=TaskStatus.PENDING,
        version_counter=1
    )

    # Save to database
    await db._save_state_sequential(state, is_milestone=False, summary=None)
    print(f"✓ Created test task: {test_task_id}")

    # Clear cache to ensure fair test
    await cache_manager.delete(f"{cache_manager.PREFIX_TASK_STATE}{test_task_id}")

    # First load - cache miss
    print("\n1. First load (cache MISS - queries database):")
    start = time.time()
    result1 = await db.load_state(test_task_id)
    time1 = (time.time() - start) * 1000
    print(f"   Time: {time1:.2f}ms")
    print(f"   Result: {result1.task_id if result1 else 'None'}")

    # Second load - cache hit
    print("\n2. Second load (cache HIT - from Redis):")
    start = time.time()
    result2 = await db.load_state(test_task_id)
    time2 = (time.time() - start) * 1000
    print(f"   Time: {time2:.2f}ms")
    print(f"   Result: {result2.task_id if result2 else 'None'}")

    # Multiple loads to show consistent performance
    print("\n3. Multiple subsequent loads (all from cache):")
    times = []
    for i in range(5):
        start = time.time()
        await db.load_state(test_task_id)
        times.append((time.time() - start) * 1000)

    avg_time = sum(times) / len(times)
    print(f"   Average time: {avg_time:.2f}ms")
    print(f"   Min time: {min(times):.2f}ms")
    print(f"   Max time: {max(times):.2f}ms")

    # Calculate speedup
    speedup = time1 / avg_time if avg_time > 0 else 0
    print(f"\n📊 Performance Improvement: {speedup:.1f}x faster")
    print(f"   Database query: {time1:.2f}ms")
    print(f"   Cached query: {avg_time:.2f}ms")

    # Show cache metrics
    metrics = cache_manager.metrics
    print(f"\n📈 Cache Metrics:")
    print(f"   Hit rate: {metrics.hit_rate:.1f}%")
    print(f"   Hits: {metrics.hits}")
    print(f"   Misses: {metrics.misses}")

    # Cleanup
    await cache_manager.delete(f"{cache_manager.PREFIX_TASK_STATE}{test_task_id}")
    print("\n✓ Benchmark complete")


async def benchmark_user_memory_caching():
    """Benchmark user memory retrieval with and without caching."""
    print("\n" + "="*60)
    print("BENCHMARK: User Memory Retrieval")
    print("="*60)

    memory_manager = MemoryManager()
    test_user_id = f"benchmark-user-{int(time.time())}"

    # Create test user memory
    user_memory = UserMemory(
        user_id=test_user_id,
        profile=UserProfile(
            user_id=test_user_id,
            role="developer",
            communication_style="technical"
        ),
        preferences=UserPreferences(
            document_tone="professional",
            detail_level="high"
        )
    )

    await memory_manager.save_user_memory(user_memory)
    print(f"✓ Created test user memory: {test_user_id}")

    # Clear cache
    await cache_manager.delete(f"{cache_manager.PREFIX_USER_MEMORY}{test_user_id}")

    # First load - cache miss
    print("\n1. First load (cache MISS):")
    start = time.time()
    result1 = await memory_manager.get_user_memory(test_user_id)
    time1 = (time.time() - start) * 1000
    print(f"   Time: {time1:.2f}ms")

    # Second load - cache hit
    print("\n2. Second load (cache HIT):")
    start = time.time()
    result2 = await memory_manager.get_user_memory(test_user_id)
    time2 = (time.time() - start) * 1000
    print(f"   Time: {time2:.2f}ms")

    # Multiple loads
    times = []
    for _ in range(5):
        start = time.time()
        await memory_manager.get_user_memory(test_user_id)
        times.append((time.time() - start) * 1000)

    avg_time = sum(times) / len(times)
    speedup = time1 / avg_time if avg_time > 0 else 0

    print(f"\n📊 Performance Improvement: {speedup:.1f}x faster")
    print(f"   Database query: {time1:.2f}ms")
    print(f"   Cached query: {avg_time:.2f}ms")

    # Cleanup
    await cache_manager.delete(f"{cache_manager.PREFIX_USER_MEMORY}{test_user_id}")
    print("\n✓ Benchmark complete")


async def demonstrate_cache_invalidation():
    """Demonstrate automatic cache invalidation."""
    print("\n" + "="*60)
    print("DEMO: Cache Invalidation")
    print("="*60)

    db = DatabaseAdapter()
    test_task_id = f"invalidation-test-{int(time.time())}"

    # Create and cache a task
    state = TaskStateSchema(
        task_id=test_task_id,
        user_id="test-user",
        goal=Goal(request="Test invalidation", success_criteria=[]),
        status=TaskStatus.PENDING,
        version_counter=1
    )

    await db._save_state_sequential(state, is_milestone=False, summary=None)
    print(f"✓ Created task: {test_task_id}")

    # Load to populate cache
    await db.load_state(test_task_id)
    print("✓ Task cached")

    # Verify it's cached
    cache_key = f"{cache_manager.PREFIX_TASK_STATE}{test_task_id}"
    cached = await cache_manager.get(cache_key)
    print(f"✓ Cache contains task: {cached is not None}")

    # Update task (should invalidate cache)
    state.status = TaskStatus.EXECUTING
    await db._save_state_sequential(state, is_milestone=False, summary=None)
    print("✓ Task updated")

    # Check if cache was invalidated
    cached_after = await cache_manager.get(cache_key)
    print(f"✓ Cache invalidated: {cached_after is None}")

    # Load again (should re-cache with new data)
    reloaded = await db.load_state(test_task_id)
    print(f"✓ Reloaded task status: {reloaded.status if reloaded else 'None'}")

    # Cleanup
    await cache_manager.delete(cache_key)
    print("\n✓ Demo complete")


async def show_cache_statistics():
    """Display comprehensive cache statistics."""
    print("\n" + "="*60)
    print("CACHE STATISTICS")
    print("="*60)

    info = await cache_manager.get_cache_info()

    print(f"\nCache Status:")
    print(f"  Enabled: {info['enabled']}")
    print(f"  Initialized: {info['initialized']}")

    if info.get('metrics'):
        metrics = info['metrics']
        print(f"\nPerformance Metrics:")
        print(f"  Hit Rate: {metrics['hit_rate']:.2f}%")
        print(f"  Cache Hits: {metrics['hits']}")
        print(f"  Cache Misses: {metrics['misses']}")
        print(f"  Errors: {metrics['errors']}")
        print(f"  Avg Time (Cached): {metrics['avg_time_cached_ms']:.2f}ms")
        print(f"  Avg Time (Uncached): {metrics['avg_time_uncached_ms']:.2f}ms")

    if info.get('redis'):
        redis_info = info['redis']
        print(f"\nRedis Statistics:")
        print(f"  Total Connections: {redis_info.get('total_connections_received', 'N/A')}")
        print(f"  Total Commands: {redis_info.get('total_commands_processed', 'N/A')}")
        print(f"  Keyspace Hits: {redis_info.get('keyspace_hits', 'N/A')}")
        print(f"  Keyspace Misses: {redis_info.get('keyspace_misses', 'N/A')}")


async def main():
    """Run all demonstrations."""
    print("\n" + "="*60)
    print("Redis Caching Performance Demo")
    print("="*60)
    print("\nThis demo will:")
    print("1. Benchmark task state retrieval")
    print("2. Benchmark user memory retrieval")
    print("3. Demonstrate cache invalidation")
    print("4. Show cache statistics")
    print("\nMake sure Redis is running: redis-cli ping")
    print("="*60)

    input("\nPress Enter to start...")

    try:
        # Run benchmarks
        await benchmark_task_state_caching()
        await benchmark_user_memory_caching()
        await demonstrate_cache_invalidation()
        await show_cache_statistics()

        print("\n" + "="*60)
        print("✓ All demos completed successfully!")
        print("="*60)

    except Exception as e:
        print(f"\n❌ Error during demo: {str(e)}")
        logger.error(f"Demo error: {str(e)}", exc_info=True)

    finally:
        # Cleanup
        await cache_manager.close()


if __name__ == "__main__":
    asyncio.run(main())
