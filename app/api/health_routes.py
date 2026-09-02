from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def home():
    return {
        "application": "FraudShield AI Enterprise",
        "version": "2.0",
        "status": "Running"
    }


@router.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "FraudShield AI Enterprise",
        "version": "2.0",
        "database": "connected"
    }


@router.get("/version")
def version():
    return {
        "version": "2.0",
        "api": "v2",
        "ml_pipeline": "Enterprise",
        "database": "MongoDB",
        "status": "Running"
    }
