import time
from typing import Dict, Tuple, Optional
from fastapi import Request, status
from fastapi.responses import JSONResponse
from src.utils.logger import logger
from src.cache.redis_cache import cache_manager
from src.core.config import settings

class RateLimiter:
    """
    Distributed rate limiting logic using Redis.
    Falls back to in-memory limiting if Redis is unavailable.
    """
    def __init__(self, requests_per_minute: int = None):
        self.requests_per_minute = requests_per_minute or settings.ratelimit.requests_per_minute
        self.PREFIX = "ratelimit:"
        # Fallback dictionary for when Redis is disabled
        self.fallback_buckets: Dict[Tuple[str, str], Tuple[int, float]] = {}

    async def is_rate_limited(self, identifier: str, endpoint: str) -> bool:
        now = time.time()
        key = f"{self.PREFIX}{identifier}:{endpoint}"

        # 1. Try Redis first if enabled
        if cache_manager.enabled and cache_manager._initialized:
            try:
                # Use Redis INCR and EXPIRE for atomic rate limiting
                current = await cache_manager.client.get(key)
                if current is None:
                    # First request in the window
                    pipe = cache_manager.client.pipeline()
                    await pipe.set(key, 1, ex=60).execute()
                    return False

                count = int(current)
                if count >= self.requests_per_minute:
                    return True

                await cache_manager.client.incr(key)
                return False
            except Exception as e:
                logger.warning(f"Redis rate limiting failed, using fallback: {e}")

        # 2. Fallback to in-memory limiting
        mem_key = (identifier, endpoint)
        if mem_key not in self.fallback_buckets:
            self.fallback_buckets[mem_key] = (1, now + 60)
            return False

        count, reset_time = self.fallback_buckets[mem_key]
        if now > reset_time:
            self.fallback_buckets[mem_key] = (1, now + 60)
            return False

        if count >= self.requests_per_minute:
            return True

        self.fallback_buckets[mem_key] = (count + 1, reset_time)
        return False

# Global instance
# Global instance
rate_limiter = RateLimiter()

async def rate_limit_middleware(request: Request, call_next):
    # Skip rate limiting in development mode
    from src.core.config import settings
    if not settings.ratelimit.enabled:
        return await call_next(request)
        
    # Identify by user ID if available, otherwise by client IP
    user = getattr(request.state, "user", None)
    identifier = user["id"] if isinstance(user, dict) and "id" in user else (request.client.host if request.client else "unknown")
    endpoint = request.url.path

    if await rate_limiter.is_rate_limited(identifier, endpoint):
        logger.warning(f"Rate limit exceeded for {identifier} on {endpoint}")
        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content={"detail": "Rate limit exceeded. Please try again later."}
        )

    return await call_next(request)
