from fastapi import Security, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.core.config import settings

security = HTTPBearer()

async def get_current_user(auth: HTTPAuthorizationCredentials = Security(security)):
    """
    Validates the bearer token and returns the user identity.
    In a real implementation, this would decode a JWT or check a session store.
    """
    token = auth.credentials

    # For dev purposes, allow any token if in debug mode
    if getattr(settings.app, "debug", False):
        return {"id": "usr_api_key_user", "role": "developer"}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Bearer token authentication is not fully implemented. Use API Key.",
        headers={"WWW-Authenticate": "Bearer"},
    )
