import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from app.api.routes import router
from app.api.auth_routes import router as auth_router
from app.api.user_routes import router as user_router
from app.continuous_learning.feedback_routes import router as feedback_router
from app.api.middleware.logging_middleware import LoggingMiddleware
from app.api.exceptions import global_exception_handler
from app.config.logging_config import logger
from app.monitoring.prometheus import ObservabilityMetrics, router as metrics_router
from app.security.rate_limiter import RateLimiter
from contextlib import asynccontextmanager
from app.alerts.routes import router as alerts_router
from app.cases.routes import router as cases_router
from app.database.connection import MongoDBConnection
from app.database.repository import FraudRepository
from app.inference.predictor import EnterpriseFraudPredictor
from app.rules.risk_engine import EnterpriseRiskEngine
from app.xai.shap_explainer import SHAPExplainer
from app.ai.groq_report import EnterpriseFraudReporter
from app.analytics.routes import router as analytics_router
from app.services.prediction_service import PredictionService
from app.reports.routes import router as reports_router
from app.settings.routes import router as settings_router
from app.api.model_routes import router as model_router
from app.api.stream_routes import router as stream_router
from app.streaming.stream_engine import StreamEngine


@asynccontextmanager
async def lifespan(app: FastAPI):

    try:

        logger.info("=" * 60)
        logger.info("STARTING FRAUDSHIELD AI ENTERPRISE")
        logger.info("=" * 60)

        database = MongoDBConnection()

        db = database.connect_sync()

        repository = FraudRepository(db)
        if not repository.health_check():
            raise RuntimeError("MongoDB Repository is unavailable.")

        predictor = EnterpriseFraudPredictor()

        predictor.initialize()
        logger.info(
            predictor.get_model_info()
        )

        risk_engine = EnterpriseRiskEngine()
        shap = SHAPExplainer()
        if not shap.health()["loaded"]:
            logger.warning("SHAP Explainer not fully loaded - explanations will use fallback methods")
        else:
            logger.info("SHAP Explainer loaded successfully")

        reporter = EnterpriseFraudReporter()

        prediction_service = PredictionService(
            predictor,
            repository,
            risk_engine,
            shap,
            reporter
        )
        if not predictor.is_ready():
            raise RuntimeError("Prediction Engine failed to initialize.")

        app.state.database = database
        app.state.db = db
        app.state.repository = repository
        app.state.predictor = predictor
        app.state.risk_engine = risk_engine
        app.state.shap = shap
        app.state.reporter = reporter
        app.state.prediction_service = prediction_service

        # Initialize Stream Engine for Kafka-based processing
        stream_engine = StreamEngine()
        app.state.stream_engine = stream_engine

        logger.info("Application Started Successfully")
        logger.info(
            predictor.health()
        )

        logger.info(
            risk_engine.health()
        )

        logger.info(
            shap.health()
        )

        logger.info(
            reporter.health()
        )

        yield
    except Exception as e:
        logger.exception(
            f"Application Startup failed:{e}"
        )
        raise
    finally:
        logger.info("STOPPING FRAUDSHIELD AI ENTERPRISE")
        logger.info("=" * 60)

        if hasattr(app.state, "database"):

            app.state.database.close()


app = FastAPI(
    title="FraudShield AI Enterprise",
    version="2.0.0",
    lifespan=lifespan
)

default_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

frontend_env_str = f"{os.getenv('FRONTEND_ORIGINS', '')},{os.getenv('FRONTEND_URL', '')}"
env_origins = [
    origin.strip().rstrip("/")
    for origin in frontend_env_str.split(",")
    if origin.strip()
]

allowed_origins = list(dict.fromkeys(default_origins + env_origins))

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_origin_regex=r"https://.*\.vercel\.app",
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
async def observability_middleware(request: Request, call_next):

    rate_limiter.check(request)

    ObservabilityMetrics.record_request(request.url.path)

    response = await call_next(request)

    if response.status_code >= 500:
        ObservabilityMetrics.record_error()

    return response


app.include_router(router)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(feedback_router)
app.include_router(metrics_router)
app.include_router(alerts_router)
app.include_router(cases_router)
app.include_router(analytics_router)
app.include_router(reports_router)
app.include_router(settings_router)
app.include_router(model_router)
app.include_router(stream_router)


@app.get("/")
def home():
    return {
        "application": "FraudShield AI Enterprise",
        "version": "2.0",
        "status": "Running"
    }


@app.get("/health")
def health(request: Request):
    predictor = getattr(request.app.state, "predictor", None)
    repository = getattr(request.app.state, "repository", None)
    risk_engine = getattr(request.app.state, "risk_engine", None)
    shap = getattr(request.app.state, "shap", None)
    reporter = getattr(request.app.state, "reporter", None)

    return {
        "status": "healthy",
        "database": repository.health_check() if repository else True,
        "model": predictor.health() if predictor else {"status": "ok"},
        "predictor": predictor.health() if predictor else {"status": "ok"},
        "risk_engine": risk_engine.health() if risk_engine else {"status": "ok"},
        "shap": shap.health() if shap else {"status": "ok"},
        "groq": reporter.health() if reporter else {"status": "ok"},
        "version": "2.0"
    }


@app.get("/version")
def version(request: Request):
    predictor = getattr(request.app.state, "predictor", None)
    if predictor:
        return predictor.get_model_info()
    return {"version": "2.0.0", "status": "standalone"}