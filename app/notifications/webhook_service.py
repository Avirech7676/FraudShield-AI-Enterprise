import requests
from app.config.logging_config import logger
from app.notifications.config import WEBHOOK_URL

class WebhookService:
    @staticmethod
    def send(message):
        if not WEBHOOK_URL:
            logger.info("Webhook URL is not configured. Webhook alert skipped.")
            return True
            
        logger.info(f"Triggering Webhook alert to {WEBHOOK_URL}")
        try:
            response = requests.post(
                WEBHOOK_URL,
                json={
                    "event": "fraud_alert",
                    "message": message
                },
                timeout=10
            )
            response.raise_for_status()
        except Exception as e:
            logger.error(f"Failed to trigger Webhook: {e}")
            raise
        return True
