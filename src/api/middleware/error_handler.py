from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from src.utils.logger import logger
import traceback

async def error_handler_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except HTTPException as exc:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )
    except Exception as exc:
        logger.exception(f"Unhandled exception: {str(exc)}")
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Internal server error",
                "message": str(exc),
                "traceback": traceback.format_exc() if logger.level == "DEBUG" else None
            }
        )
