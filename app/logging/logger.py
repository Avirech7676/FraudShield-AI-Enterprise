# ---------------------------------------------------------------------------
# app/logging/logger.py
# Compatibility wrapper — delegates to the single canonical logger defined in
# app.config.logging_config so every module uses the same underlying handler.
# ---------------------------------------------------------------------------
from app.config.logging_config import logger as _logger


class EnterpriseLogger:
    """Backward-compatible static wrapper around the canonical logger."""

    @staticmethod
    def info(message: str) -> None:
        _logger.info(message)

    @staticmethod
    def warning(message: str) -> None:
        _logger.warning(message)

    @staticmethod
    def error(message: str) -> None:
        _logger.error(message)

    @staticmethod
    def exception(message: str) -> None:
        _logger.exception(message)

    @staticmethod
    def debug(message: str) -> None:
        _logger.debug(message)