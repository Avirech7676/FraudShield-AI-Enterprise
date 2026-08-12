import os
from dotenv import load_dotenv
from pathlib import Path

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
        "JWT_SECRET_KEY",
        "dev-secret-key-change-in-production"
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
    BASE_DIR = Path(__file__).resolve().parents[2]
    MODEL_DIRECTORY = BASE_DIR / os.getenv("MODEL_DIRECTORY", "models")

    MODEL_VERSION = os.getenv(
        "MODEL_VERSION",
        os.getenv("DEFAULT_MODEL_VERSION", "2.0")
    )

    DEFAULT_MODEL_VERSION = os.getenv(
        "DEFAULT_MODEL_VERSION",
        MODEL_VERSION
    )

    PRODUCTION_MODEL = MODEL_DIRECTORY / "production_model.joblib"
    BEST_MODEL = MODEL_DIRECTORY /  "best_model.joblib"
    PREPROCESSOR = MODEL_DIRECTORY / "preprocessor.joblib"


    #####################################################
    # Dataset
    #####################################################

    DATASET = os.getenv("DATASET", "data/raw/creditcard.csv")

    #####################################################
    # Logging
    #####################################################

    LOG_DIRECTORY = BASE_DIR / os.getenv("LOG_DIRECTORY", "logs")

    REPORT_DIRECTORY = BASE_DIR / os.getenv("REPORT_DIRECTORY", "reports")

    MODEL_DIRECTORY.mkdir(parents=True, exist_ok=True)

    LOG_DIRECTORY.mkdir(parents=True, exist_ok=True)

    REPORT_DIRECTORY.mkdir(parents=True, exist_ok=True)
    #####################################################
    # Thresholds
    #####################################################

    FRAUD_THRESHOLD = 0.50

    RETRAIN_THRESHOLD = 100

    #####################################################
    # API
    #####################################################

    HOST = "0.0.0.0"

    PORT = int(os.getenv("PORT", "8000"))

    API_VERSION = os.getenv("API_VERSION", "v2")

    API_KEY = os.getenv("API_KEY")

    RATE_LIMIT_PER_MINUTE = int(
        os.getenv("RATE_LIMIT_PER_MINUTE", 60)
    )
    # Concurrency limit for async inference
    MAX_INFERENCE_CONCURRENCY = int(os.getenv("MAX_INFERENCE_CONCURRENCY", 10))

    ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")




#####################################################
# Validation
#####################################################

    def validate(self):

        required = {

            "MONGODB_URI": self.MONGODB_URI,

            "JWT_SECRET_KEY": self.JWT_SECRET_KEY

        }

        missing = [

            key

            for key, value in required.items()

            if not value

        ]

        if missing:

            raise RuntimeError(

                f"Missing environment variables: {', '.join(missing)}"

            )
settings = Settings()
settings.validate()