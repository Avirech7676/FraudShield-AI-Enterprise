import time
from collections import defaultdict, deque

from fastapi import HTTPException, Request

from app.config.settings import settings


class RateLimiter:
    def __init__(self, limit_per_minute=None):
        self.limit_per_minute = limit_per_minute or settings.RATE_LIMIT_PER_MINUTE
        self.requests = defaultdict(deque)

    def check(self, request: Request):
        client = request.client.host if request.client else "unknown"
        now = time.time()
        window = self.requests[client]

        while window and now - window[0] > 60:
            window.popleft()

        if len(window) >= self.limit_per_minute:
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded"
            )

        window.append(now)
        return True
