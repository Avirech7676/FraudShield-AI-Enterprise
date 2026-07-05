from app.notifications.email_service import EmailService
from app.notifications.telegram_service import TelegramService
from app.notifications.slack_service import SlackService
from app.notifications.teams_service import TeamsService

class NotificationManager:

    @staticmethod
    def notify(prediction):

        message = f"""
Fraud Alert

Transaction: {prediction['transaction_id']}

Risk Score: {prediction['risk_score']}

Priority: P1

Prediction: {prediction['prediction']}
"""

        TelegramService.send(message)

        SlackService.send(message)

        TeamsService.send(message)

        # Optional email
        # EmailService.send(
        #     "Fraud Alert",
        #     message,
        #     "security@company.com"
        # )