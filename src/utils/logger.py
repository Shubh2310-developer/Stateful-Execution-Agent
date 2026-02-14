import logging
import sys
from typing import Any, Dict

from loguru import logger
from src.core.config import settings


def reasoning_filter(record: Dict[str, Any]) -> bool:
    """Filter for reasoning logs."""
    return record["extra"].get("reasoning", False)


def standard_filter(record: Dict[str, Any]) -> bool:
    """Filter for standard logs."""
    return not record["extra"].get("reasoning", False)


def setup_logging():
    """Setup structured logging using Loguru."""
    # Remove default handler
    logger.remove()

    is_production = settings.app.env == "production"

    # Standard Application Logs
    if is_production:
        # JSON output for production
        logger.add(
            sys.stdout,
            filter=standard_filter,
            format="{message}",
            serialize=True,
            level="INFO",
        )
    else:
        # Tinted text for development
        logger.add(
            sys.stdout,
            filter=standard_filter,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level> [task_id={extra[task_id]}] [step_id={extra[step_id]}]",
            colorize=True,
            level="DEBUG",
        )

    # Reasoning Logs
    reasoning_format = (
        "REASONING | {time:YYYY-MM-DD HH:mm:ss} | {message} | "
        "task_id={extra[task_id]} | step_id={extra[step_id]}"
    )

    if is_production:
        logger.add(
            "logs/reasoning.json",
            filter=reasoning_filter,
            serialize=True,
            level="DEBUG",
            rotation="100 MB",
        )
    else:
        logger.add(
            sys.stdout,
            filter=reasoning_filter,
            format=f"<magenta>{reasoning_format}</magenta>",
            colorize=True,
            level="DEBUG",
        )

    # File handler for errors
    logger.add(
        "logs/error.log",
        level="ERROR",
        rotation="10 MB",
        retention="1 month",
        compression="zip",
        serialize=is_production,
    )

    # Intercept standard logging
    class InterceptHandler(logging.Handler):
        def emit(self, record):
            try:
                level = logger.level(record.levelname).name
            except ValueError:
                level = record.levelno

            frame, depth = logging.currentframe(), 2
            while frame.f_code.co_filename == logging.__file__:
                frame = frame.f_back
                depth += 1

            logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())

    logging.basicConfig(handlers=[InterceptHandler()], level=0)

    # Bind default context
    logger.configure(extra={"task_id": "none", "step_id": "none", "reasoning": False})


# Initialize logging
setup_logging()


def get_logger(task_id: str = "none", step_id: str = "none"):
    """Get a context-aware logger."""
    return logger.bind(task_id=task_id, step_id=step_id)


def get_reasoning_logger(task_id: str = "none", step_id: str = "none"):
    """Get a context-aware reasoning logger."""
    return logger.bind(task_id=task_id, step_id=step_id, reasoning=True)
