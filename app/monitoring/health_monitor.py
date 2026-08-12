from app.monitoring.system_monitor import SystemMonitor


class HealthMonitor:
    def __init__(self):
        self.system_monitor = SystemMonitor()

    def check(self):
        snapshot = self.system_monitor.snapshot()
        status = "healthy"

        if snapshot["mongodb"] != "Online":
            status = "degraded"

        if snapshot["memory_usage"] >= 90 or snapshot["disk_usage"] >= 90:
            status = "critical"

        return {
            "status": status,
            "service": "FraudShield AI Enterprise",
            "version": "2.0",
            "checks": snapshot
        }
