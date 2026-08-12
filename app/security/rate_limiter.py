import time
from collections import defaultdict, deque
from fastapi import HTTPException, Request
from app.config.settings import settings


class RateLimiter:
    def __init__(self, limit_per_minute=None):
        self.limit_per_minute = limit_per_minute or settings.RATE_LIMIT_PER_MINUTE
        self.requests = defaultdict(deque)
        self._last_cleanup = time.time()

    def _cleanup_stale_clients(self, now: float):
        # Periodically purge stale IP entries older than 5 minutes to prevent memory leaks
        if now - self._last_cleanup > 300:
            stale_ips = [
                ip for ip, window in self.requests.items()
                if not window or (now - window[-1] > 300)
            ]
            for ip in stale_ips:
                del self.requests[ip]
            self._last_cleanup = now

    def check(self, request: Request):
        client = request.client.host if (request.client and request.client.host) else "unknown"
        now = time.time()
        window = self.requests[client]

        while window and now - window[0] > 60:
            window.popleft()

        if len(window) >= self.limit_per_minute:
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded. Please slow down request rate."
            )

        window.append(now)
        self._cleanup_stale_clients(now)
        return True
