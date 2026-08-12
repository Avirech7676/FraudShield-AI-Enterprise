from app.config.logging_config import logger


class AlertManager:
    def __init__(self, notification_manager=None):
        self.notification_manager = notification_manager

    def evaluate_system_alerts(self, health_snapshot):
        alerts = []
        checks = health_snapshot.get("checks", {})

        if checks.get("mongodb") != "Online":
            alerts.append(("P1", "MongoDB is offline"))

        if checks.get("memory_usage", 0) >= 90:
            alerts.append(("P2", "Memory usage is above 90 percent"))

        if checks.get("disk_usage", 0) >= 90:
            alerts.append(("P2", "Disk usage is above 90 percent"))

        for priority, message in alerts:
            logger.warning("%s observability alert: %s", priority, message)
            if self.notification_manager:
                self.notification_manager.send(
                    subject="FraudShield Observability Alert",
                    message=message,
                    priority=priority
                )

        return alerts
