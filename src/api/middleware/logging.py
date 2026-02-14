import time
from fastapi import Request
from src.utils.logger import logger

async def logging_middleware(request: Request, call_next):
    start_time = time.time()

    path = request.url.path
    method = request.method

    logger.info(f"Incoming request: {method} {path}")

    response = await call_next(request)

    process_time = time.time() - start_time
    status_code = response.status_code

    logger.info(f"Request completed: {method} {path} - Status: {status_code} - Duration: {process_time:.4f}s")

    return response
