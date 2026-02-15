"""
Cache lifecycle management for integration with FastAPI application.

Handles cache initialization and cleanup during app startup/shutdown.
"""

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from src.cache.redis_cache import cache_manager
from src.utils.logger import logger


@asynccontextmanager
async def cache_lifespan(app: FastAPI) -> AsyncIterator[None]:
    """
    Lifespan context manager for cache initialization and cleanup.

    Usage:
        app = FastAPI(lifespan=cache_lifespan)
    """
    # Startup: Initialize cache
    logger.info("Initializing Redis cache...")
    try:
        await cache_manager.initialize()
        logger.info("Redis cache initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize cache: {str(e)}")
        logger.warning("Application will continue without cache")

    yield

    # Shutdown: Close cache connections
    logger.info("Shutting down Redis cache...")
    try:
        await cache_manager.close()
        logger.info("Redis cache shutdown complete")
    except Exception as e:
        logger.error(f"Error during cache shutdown: {str(e)}")


async def initialize_cache():
    """
    Initialize cache during application startup.

    Can be used as a startup event handler.
    """
    logger.info("Initializing Redis cache...")
    try:
        await cache_manager.initialize()
        logger.info("Redis cache initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize cache: {str(e)}")
        logger.warning("Application will continue without cache")


async def shutdown_cache():
    """
    Shutdown cache during application shutdown.

    Can be used as a shutdown event handler.
    """
    logger.info("Shutting down Redis cache...")
    try:
        # Log final statistics before shutdown
        cache_manager.metrics.log_stats()
        await cache_manager.close()
        logger.info("Redis cache shutdown complete")
    except Exception as e:
        logger.error(f"Error during cache shutdown: {str(e)}")
