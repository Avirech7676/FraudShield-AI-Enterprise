# FraudShield AI Enterprise application package.
#
# NOTE: Do NOT import the FastAPI app here (e.g. `from app.api.main import app`).
# Doing so makes importing ANY submodule (features, ml, utils) load the whole
# API — which constructs the predictor and tries to load model files. That
# creates a circular dependency: you cannot run train.py to CREATE the model
# because importing `app` requires the model to already exist.
#
# The application entrypoint is `app.api.main:app` (used by uvicorn/gunicorn).
