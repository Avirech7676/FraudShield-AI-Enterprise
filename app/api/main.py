import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.health_routes import router as health_router
from app.api.prediction_routes import router as prediction_router
from app.api.dashboard_routes import router as dashboard_router
from app.api.admin_routes import router as admin_router
from app.api.feedback_routes import router as feedback_router
from app.api.case_routes import router as case_router
from app.api.auth_routes import router as auth_router
from app.api.user_routes import router as user_router
from app.api.middleware.logging_middleware import LoggingMiddleware
from app.api.exceptions import global_exception_handler
from app.config.logging_config import logger
from app.monitoring.prometheus import ObservabilityMetrics, router as metrics_router
from app.security.rate_limiter import RateLimiter


# ---------------------------------------------------------------------------
# CORS — reads from ALLOWED_ORIGINS env var (comma-separated) at runtime.
# Falls back to the standard local + production origins when not set.
# ---------------------------------------------------------------------------
_default_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:4173",
    "http://127.0.0.1:4173",
    "https://fraud-shield-ai-enterprise.vercel.app",
]
_env_origins = os.getenv("ALLOWED_ORIGINS", "")
ALLOWED_ORIGINS = (
    [o.strip() for o in _env_origins.split(",") if o.strip()]
    if _env_origins
    else _default_origins
)

app = FastAPI(
    title="FraudShield AI Enterprise",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    LoggingMiddleware
)

app.add_exception_handler(
    Exception,
    global_exception_handler
)

rate_limiter = RateLimiter()


@app.middleware("http")
async def observability_middleware(request, call_next):
    rate_limiter.check(request)
    ObservabilityMetrics.record_request(request.url.path)

    response = await call_next(request)

    if response.status_code >= 500:
        ObservabilityMetrics.record_error()

    return response


# Register Routers
app.include_router(health_router)
app.include_router(prediction_router)
app.include_router(dashboard_router)
app.include_router(admin_router)
app.include_router(feedback_router)
app.include_router(case_router)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(metrics_router)
