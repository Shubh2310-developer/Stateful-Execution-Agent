from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import tasks, health, state, artifacts, memory, trace
from src.api.middleware.logging import logging_middleware
from src.api.middleware.error_handler import error_handler_middleware
from src.core.config import settings
from src.utils.logger import logger

app = FastAPI(
    title=settings.APP_NAME,
    description="Stateful Execution Agent API",
    version="1.0.0",
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
app.include_router(tasks.router, prefix=settings.API_V1_STR)
app.include_router(health.router, prefix=settings.API_V1_STR)
app.include_router(state.router, prefix=settings.API_V1_STR)
app.include_router(artifacts.router, prefix=settings.API_V1_STR)
app.include_router(memory.router, prefix=settings.API_V1_STR)
app.include_router(trace.router, prefix=settings.API_V1_STR)

@app.on_event("startup")
async def startup_event():
    logger.info(f"Starting up {settings.APP_NAME} in {settings.ENV} mode")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info(f"Shutting down {settings.APP_NAME}")

@app.get("/")
async def root():
    return {
        "app": settings.APP_NAME,
        "version": "1.0.0",
        "status": "online"
    }
