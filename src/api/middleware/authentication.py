from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from src.api.dependencies.auth import get_current_user
from src.utils.logger import logger
from src.core.config import settings

async def authentication_middleware(request: Request, call_next):
    """
    Middleware for global authentication checks.
    Ensures that a valid token is provided for protected routes.
    """
    # Skip auth for health check, root, and docs
    public_paths = [
        "/",
        f"{settings.app.api_v1_str}/health",
        "/docs",
        "/openapi.json",
        "/redoc"
    ]

    if request.url.path == "/" or any(request.url.path.startswith(path) for path in public_paths if path != "/"):
        return await call_next(request)

    # Check for Authorization header (Bearer) or API Key
    auth_header = request.headers.get("Authorization")
    api_key_header = request.headers.get(settings.security.api_key_header)

    if not auth_header and not api_key_header:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Missing authentication credentials"},
            headers={"WWW-Authenticate": "Bearer, ApiKey"},
        )

    try:
        user_id = "unknown"

        # 1. API Key Authentication
        if api_key_header:
            if api_key_header != settings.security.api_key:
                 raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API Key")
            user_id = "usr_api_key_user"

        # 2. Bearer Token Authentication
        elif auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            # In a real system, this would validate a JWT or session token
            # For this implementation, we rely on the API Key or Debug mode
            if not getattr(settings.app, "debug", False):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Bearer token authentication is not fully implemented. Use API Key.")
            user_id = "usr_api_key_user"
        else:
             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication scheme")

        # Attach user info to request state
        request.state.user = {"id": user_id}

    except HTTPException as he:
        # Re-raise HTTP exceptions to let them propagate (or handle them if you prefer JSONResponse)
        if he.status_code == 401:
             return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": he.detail},
                headers={"WWW-Authenticate": "Bearer, ApiKey"},
            )
        raise he
    except Exception as e:
        logger.error(f"Authentication failed: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Authentication failed"},
            headers={"WWW-Authenticate": "Bearer, ApiKey"},
        )

    return await call_next(request)
