import os
from dotenv import load_dotenv

load_dotenv()


class Settings:

    #####################################################
    # Database
    #####################################################

    MONGODB_URI = os.getenv(
        "MONGODB_URI",
        "mongodb://localhost:27017"
    )

    DATABASE_NAME = os.getenv(
        "DATABASE_NAME",
        "FraudShieldDB"
    )

    #####################################################
    # Authentication
    #####################################################

    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY"
    )

    JWT_ALGORITHM = os.getenv(
        "JWT_ALGORITHM",
        "HS256"
    )

    JWT_EXPIRE_MINUTES = int(
        os.getenv(
            "JWT_EXPIRE_MINUTES",
            60
        )
    )

    #####################################################
    # AI
    #####################################################

    GROQ_API_KEY = os.getenv(
        "GROQ_API_KEY"
    )

    #####################################################
    # Model
    #####################################################

    MODEL_DIRECTORY = os.getenv("MODEL_DIRECTORY", "models")

    MODEL_VERSION = os.getenv(
        "MODEL_VERSION",
        os.getenv("DEFAULT_MODEL_VERSION", "2.0")
    )

    DEFAULT_MODEL_VERSION = os.getenv(
        "DEFAULT_MODEL_VERSION",
        MODEL_VERSION
    )

    PRODUCTION_MODEL = os.path.join(
        MODEL_DIRECTORY,
        "production_model.joblib"
    )

    BEST_MODEL = os.path.join(
        MODEL_DIRECTORY,
        "best_model.joblib"
    )

    PREPROCESSOR = os.path.join(
        MODEL_DIRECTORY,
        "preprocessor.joblib"
    )

    #####################################################
    # Dataset
    #####################################################

    DATASET = os.getenv("DATASET", "data/raw/creditcard.csv")

    #####################################################
    # Logging
    #####################################################

    LOG_DIRECTORY = os.getenv("LOG_DIRECTORY", "logs")

    REPORT_DIRECTORY = os.getenv("REPORT_DIRECTORY", "reports")

    #####################################################
    # Thresholds
    #####################################################

    FRAUD_THRESHOLD = 0.50

    RETRAIN_THRESHOLD = 100

    #####################################################
    # API
    #####################################################

    HOST = "0.0.0.0"

    PORT = 8000

    API_VERSION = os.getenv("API_VERSION", "v2")

    API_KEY = os.getenv("API_KEY")

    RATE_LIMIT_PER_MINUTE = int(
        os.getenv("RATE_LIMIT_PER_MINUTE", 60)
    )

    ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")


settings = Settings()
