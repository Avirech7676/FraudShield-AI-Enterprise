from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def home():
    return {
        "Application": "FraudShield AI Enterprise",
        "Status": "Running"
    }


@router.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "FraudShield AI Enterprise",
        "version": "2.0"
    }


@router.get("/version")
def version():
    return {
        "api": "v2",
        "ml_pipeline": "Enterprise",
        "database": "MongoDB",
        "status": "Running"
    }
