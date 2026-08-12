import time
import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.config.logging_config import logger


class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        request_id = str(uuid.uuid4())

        start = time.perf_counter()

        logger.info("=" * 70)
        logger.info(f"Request ID : {request_id}")
        logger.info(f"Method     : {request.method}")
        logger.info(f"Path       : {request.url.path}")

        response = await call_next(request)

        latency = round(

            (time.perf_counter() - start) * 1000,

            2

        )

        logger.info(f"Status     : {response.status_code}")
        logger.info(f"Latency    : {latency} ms")
        logger.info("=" * 70)

        response.headers["X-Request-ID"] = request_id

        return response
