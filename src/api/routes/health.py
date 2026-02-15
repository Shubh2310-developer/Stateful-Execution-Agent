from fastapi import APIRouter
from src.core.config import settings
from src.cache.redis_cache import cache_manager

router = APIRouter(prefix="/health", tags=["health"])

@router.get("")
async def health_check():
    """Basic health check endpoint."""
    return {
        "status": "healthy",
        "app": settings.app.name,
        "environment": settings.app.env
    }

@router.get("/cache")
async def cache_health():
    """Cache health and performance metrics endpoint."""
    cache_info = await cache_manager.get_cache_info()
    return cache_info
