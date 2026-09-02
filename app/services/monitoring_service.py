from app.monitoring.prometheus import ObservabilityMetrics


class MonitoringService:
    """
    Monitoring Service Layer
    Wraps Prometheus and Observability metrics collection.
    """

    @staticmethod
    def record_request(path):
        ObservabilityMetrics.record_request(path)

    @staticmethod
    def record_error():
        ObservabilityMetrics.record_error()
