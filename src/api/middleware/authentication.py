from fastapi import Request, HTTPException
from src.api.dependencies.auth import get_current_user
from src.utils.logger import logger

async def authentication_middleware(request: Request, call_next):
    """
    Middleware for global authentication checks if needed.
    Currently, we prefer dependency injection per route.
    """
    # Example: Skip auth for health check and root
    if request.url.path in ["/", "/api/v1/health"]:
        return await call_next(request)

    # For other routes, logging the user (actual check in dependencies)
    return await call_next(request)
