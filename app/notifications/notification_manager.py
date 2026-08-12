from app.notifications.email_service import EmailService
from app.notifications.telegram_service import TelegramService
from app.notifications.slack_service import SlackService
from app.notifications.teams_service import TeamsService
from app.notifications.sms_service import SMSService
from app.notifications.webhook_service import WebhookService
from app.config.logging_config import logger


class NotificationManager:
    history = []
    templates = {
        "fraud_alert": (
            "Fraud Alert\n\n"
            "Transaction: {transaction_id}\n"
            "Risk Score: {risk_score}\n"
            "Priority: {priority}\n"
            "Prediction: {prediction}"
        ),
        "system_alert": "{subject}\n\n{message}"
    }

    @classmethod
    def _record(cls, channel, priority, message, success, error=None):
        item = {
            "channel": channel,
            "priority": priority,
            "message": message,
            "success": success,
            "error": error
        }
        cls.history.append(item)
        return item

    @classmethod
    def _send_with_retry(cls, channel, sender, message, priority, attempts=3):
        last_error = None
        for attempt in range(1, attempts + 1):
            try:
                sender(message)
                cls._record(channel, priority, message, True)
                return True
            except Exception as exc:
                last_error = str(exc)
                logger.warning(
                    "Notification attempt failed | channel=%s | attempt=%s | error=%s",
                    channel,
                    attempt,
                    last_error
                )

        cls._record(channel, priority, message, False, last_error)
        logger.error("Notification failed | channel=%s | error=%s", channel, last_error)
        return False

    @classmethod
    def send(cls, subject, message, priority="P3", receiver=None):
        formatted = cls.templates["system_alert"].format(
            subject=subject,
            message=message
        )
        channels = {
            "P1": ["telegram", "slack", "teams", "email", "sms", "webhook"],
            "P2": ["slack", "teams", "webhook"],
            "P3": ["slack"]
        }.get(priority, ["slack"])

        for channel in channels:
            if channel == "telegram":
                cls._send_with_retry(channel, TelegramService.send, formatted, priority)
            elif channel == "slack":
                cls._send_with_retry(channel, SlackService.send, formatted, priority)
            elif channel == "teams":
                cls._send_with_retry(channel, TeamsService.send, formatted, priority)
            elif channel == "sms":
                cls._send_with_retry(channel, SMSService.send, formatted, priority)
            elif channel == "webhook":
                cls._send_with_retry(channel, WebhookService.send, formatted, priority)
            elif channel == "email" and receiver:
                cls._send_with_retry(
                    channel,
                    lambda body: EmailService.send(subject, body, receiver),
                    formatted,
                    priority
                )

    @staticmethod
    def notify(prediction):
        priority = prediction.get("priority", "P1")
        message = NotificationManager.templates["fraud_alert"].format(
            transaction_id=prediction["transaction_id"],
            risk_score=prediction["risk_score"],
            priority=priority,
            prediction=prediction["prediction"]
        )

        NotificationManager.send(
            subject="FraudShield Fraud Alert",
            message=message,
            priority=priority
        )
