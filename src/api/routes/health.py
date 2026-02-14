from fastapi import APIRouter
from src.core.config import settings

router = APIRouter(prefix="/health", tags=["health"])

@router.get("")
async def health_check():
    """Basic health check endpoint."""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "environment": settings.ENV
    }
