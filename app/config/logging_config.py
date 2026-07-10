import logging
import os

from app.config.settings import settings

# Create logs directory
os.makedirs(
    settings.LOG_DIRECTORY,
    exist_ok=True
)

# Create logger
logger = logging.getLogger("FraudShield")
logger.setLevel(logging.INFO)

# Prevent duplicate handlers
if not logger.handlers:

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    file_handler = logging.FileHandler(
        os.path.join(
            settings.LOG_DIRECTORY,
            "system.log"
        )
    )

    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()

    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger.propagate = False