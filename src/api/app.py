from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import tasks, health, state, artifacts, memory, trace
from src.api.middleware.logging import logging_middleware
from src.api.middleware.error_handler import error_handler_middleware
from src.core.config import settings
from src.utils.logger import logger

app = FastAPI(
    title=settings.app.name,
    description="Stateful Execution Agent API",
    version=settings.app.version,
)

# Set up Middleware
app.middleware("http")(logging_middleware)
app.middleware("http")(error_handler_middleware)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
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

@app.on_event("startup")
async def startup_event():
    logger.info(f"Starting up {settings.app.name} in {settings.app.env} mode")
    from src.tools.tool_registry import tool_registry
    tool_registry.discover_tools()

@app.on_event("shutdown")
async def shutdown_event():
    logger.info(f"Shutting down {settings.app.name}")

@app.get("/")
async def root():
    return {
        "app": settings.app.name,
        "version": settings.app.version,
        "status": "online"
    }
