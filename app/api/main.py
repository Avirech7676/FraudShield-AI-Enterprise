from fastapi import FastAPI

from app.api.routes import router
from app.api.auth_routes import router as auth_router
from app.api.user_routes import router as user_router

app = FastAPI(
    title="FraudShield AI Enterprise",
    version="1.0.0"
)

# Prediction APIs
app.include_router(router)

# Authentication APIs
app.include_router(auth_router)
app.include_router(user_router)

@app.get("/")
def home():

    return {

        "Application": "FraudShield AI Enterprise",

        "Status": "Running"

    }