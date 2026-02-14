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
    # Simulated validation
    if token == "demo-token-123":
        return {"id": "usr_demo_123", "role": "admin"}

    # For dev purposes, allow any token if in debug mode (optional safety check)
    if settings.DEBUG:
        return {"id": "usr_dev_user", "role": "developer"}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
