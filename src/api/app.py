from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import tasks, health, state, artifacts, memory, trace, websocket
from src.api.middleware.logging import logging_middleware
from src.api.middleware.trace_context import trace_context_middleware
from src.api.middleware.error_handler import error_handler_middleware
from src.api.middleware.authentication import authentication_middleware
from src.api.middleware.rate_limiting import rate_limit_middleware
from src.cache.lifecycle import initialize_cache, shutdown_cache
from src.core.config import settings
from src.utils.logger import logger

app = FastAPI(
    title=settings.app.name,
    description="Stateful Execution Agent API",
    version=settings.app.version,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Set up Middleware (Order matters: The middleware added later is executed first)
# We want: ErrorHandler -> Logging -> Auth -> RateLimit -> Endpoint
# So we add in reverse order of desired execution:
# 1. RateLimit (Innermost)
# 2. Auth (Sets user for RateLimit)
# 3. Logging (Logs authenticated requests)
# 4. ErrorHandler (Outermost, catches all errors)

app.middleware("http")(rate_limit_middleware)
app.middleware("http")(authentication_middleware)
app.middleware("http")(logging_middleware)
app.middleware("http")(trace_context_middleware)
app.middleware("http")(error_handler_middleware)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Explicitly allow frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(tasks.router, prefix=settings.app.api_v1_str)
app.include_router(health.router, prefix=settings.app.api_v1_str)
app.include_router(state.router, prefix=settings.app.api_v1_str)
app.include_router(artifacts.router, prefix=settings.app.api_v1_str)
app.include_router(memory.router, prefix=settings.app.api_v1_str)
app.include_router(trace.router, prefix=settings.app.api_v1_str)
app.include_router(websocket.router, prefix=settings.app.api_v1_str)

@app.on_event("startup")
async def startup_event():
    logger.info(f"Starting up {settings.app.name} in {settings.app.env} mode")

    # Initialize cache
    await initialize_cache()

    # Discover tools
    from src.tools.tool_registry import tool_registry
    tool_registry.discover_tools()

@app.on_event("shutdown")
async def shutdown_event():
    logger.info(f"Shutting down {settings.app.name}")

    # Shutdown cache
    await shutdown_cache()

@app.get("/")
async def root():
    return {
        "app": settings.app.name,
        "version": settings.app.version,
        "status": "online"
    }
