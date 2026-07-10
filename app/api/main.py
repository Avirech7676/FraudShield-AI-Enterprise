from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.api.auth_routes import router as auth_router
from app.api.user_routes import router as user_router
from app.continuous_learning.feedback_routes import router as feedback_router
from app.api.middleware.logging_middleware import LoggingMiddleware
from app.api.exceptions import global_exception_handler
from app.config.logging_config import logger
from app.monitoring.prometheus import ObservabilityMetrics, router as metrics_router
from app.security.rate_limiter import RateLimiter


app = FastAPI(
    title="FraudShield AI Enterprise",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:4173",
        "http://127.0.0.1:4173",
        "https://fraud-shield-ai-enterprise.vercel.app/"
    ],
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

# Prediction APIs
app.include_router(router)
app.include_router(feedback_router)
app.include_router(metrics_router)
# Authentication APIs
app.include_router(auth_router)
app.include_router(user_router)

@app.get("/")
def home():

    return {

        "Application": "FraudShield AI Enterprise",
        "Status": "Running"
    }
@app.get("/health")

def health():

    return {

        "status": "healthy",

        "service": "FraudShield AI Enterprise",

        "version": "2.0"

    }
@app.get("/version")

def version():

    return {

        "api": "v2",

        "ml_pipeline": "Enterprise",

        "database": "MongoDB",

        "status": "Running"

    }
