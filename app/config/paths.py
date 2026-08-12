import os

PROJECT_ROOT = os.getcwd()

MODELS = os.path.join(
    PROJECT_ROOT,
    "models"
)

LOGS = os.path.join(
    PROJECT_ROOT,
    "logs"
)

REPORTS = os.path.join(
    PROJECT_ROOT,
    "reports"
)

DATA = os.path.join(
    PROJECT_ROOT,
    "data"
)

RAW_DATA = os.path.join(
    DATA,
    "raw"
)

PROCESSED_DATA = os.path.join(
    DATA,
    "processed"
)
