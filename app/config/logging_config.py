import logging
import os
from logging.handlers import RotatingFileHandler
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
        "%(asctime)s | %(levelname)-8s | %(filename)s:%(lineno)d | %(message)s"
    )

    file_handler = RotatingFileHandler(
        os.path.join(
            settings.LOG_DIRECTORY,
            "system.log"
        ),
        maxBytes= 10*1024*1024,
        backupCount= 5,
        encoding= "utf-8"
    )

    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()

    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger.propagate = False
    logger.info("=" * 60)
    logger.info("FraudShield Logging Initialized")
    logger.info("=" * 60)
