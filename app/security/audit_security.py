from app.config.logging_config import logger


class SecurityAuditLogger:
    @staticmethod
    def log_event(event, user=None, metadata=None, level="info"):
        payload = {
            "event": event,
            "user": user or "anonymous",
            "metadata": metadata or {}
        }
        log = getattr(logger, level, logger.info)
        log("Security audit event: %s", payload)
