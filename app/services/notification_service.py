from app.notifications.notification_manager import NotificationManager


class NotificationService:
    """
    Notification Service Layer
    Wraps legacy NotificationManager to send high-priority alerts asynchronously.
    """

    @staticmethod
    def send_notification(subject, message, priority="P3", receiver=None):
        NotificationManager.send(subject, message, priority, receiver)

    @staticmethod
    def notify_fraud(prediction_details):
        NotificationManager.notify(prediction_details)
