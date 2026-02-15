from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from src.utils.logger import logger
from src.core.config import settings
import traceback

async def error_handler_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except HTTPException as exc:
        logger.warning(f"HTTP error: {exc.detail} - Status: {exc.status_code}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": True,
                "status_code": exc.status_code,
                "detail": exc.detail
            }
        )
    except Exception as exc:
        logger.exception(f"Unhandled exception: {str(exc)}")

        error_content = {
            "error": True,
            "status_code": 500,
            "detail": "Internal server error",
            "message": str(exc)
        }

        # Only include traceback in development environment
        if settings.app.env == "development":
            error_content["traceback"] = traceback.format_exc()

        return JSONResponse(
            status_code=500,
            content=error_content
        )
