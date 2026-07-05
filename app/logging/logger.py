import logging
import os

os.makedirs(
    "logs",
    exist_ok=True
)
logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

class EnterpriseLogger:
    @staticmethod
    def info(message):
        logging.info(message)
    @staticmethod
    def warning(message):
        logging.warning(message)
    @staticmethod
    def error(message):
        logging.error(message)