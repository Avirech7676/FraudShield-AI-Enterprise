import time
from collections import defaultdict

from fastapi import APIRouter, Response

from app.config.settings import settings
from app.monitoring.system_monitor import SystemMonitor

router = APIRouter()


class ObservabilityMetrics:
    request_count = 0
    api_error_count = 0
    prediction_count = 0
    fraud_prediction_count = 0
    prediction_latency_seconds = []
    route_counts = defaultdict(int)
    model_precision = 0.0
    model_recall = 0.0
    model_f1 = 0.0
    model_roc_auc = 0.0
    drift_score = 0.0
    started_at = time.time()

    @classmethod
    def record_request(cls, route):
        cls.request_count += 1
        cls.route_counts[route] += 1

    @classmethod
    def record_error(cls):
        cls.api_error_count += 1

    @classmethod
    def record_prediction(cls, latency_seconds, is_fraud=False):
        cls.prediction_count += 1
        cls.prediction_latency_seconds.append(latency_seconds)
        if is_fraud:
            cls.fraud_prediction_count += 1

    @classmethod
    def fraud_rate(cls):
        if cls.prediction_count == 0:
            return 0.0
        return cls.fraud_prediction_count / cls.prediction_count

    @classmethod
    def average_prediction_latency(cls):
        if not cls.prediction_latency_seconds:
            return 0.0
        return sum(cls.prediction_latency_seconds) / len(cls.prediction_latency_seconds)

    @classmethod
    def throughput_per_second(cls):
        elapsed = max(time.time() - cls.started_at, 1)
        return cls.prediction_count / elapsed


def time_prediction(func, *args, **kwargs):
    started = time.perf_counter()
    result = func(*args, **kwargs)
    latency = time.perf_counter() - started
    is_fraud = bool(
        result.get("Prediction") in {"Fraud", 1, True}
        or result.get("Fraud_Probability", 0) >= 0.5
    )
    ObservabilityMetrics.record_prediction(latency, is_fraud=is_fraud)
    return result


def render_prometheus_metrics():
    monitor = SystemMonitor()
    snapshot = monitor.snapshot()
    mongodb_up = 1 if snapshot["mongodb"] == "Online" else 0
    model_loaded = 1 if snapshot["model"] == "Loaded" else 0

    lines = [
        "# HELP fraudshield_request_count Total API requests observed.",
        "# TYPE fraudshield_request_count counter",
        f"fraudshield_request_count {ObservabilityMetrics.request_count}",
        "# HELP fraudshield_api_error_count Total API errors observed.",
        "# TYPE fraudshield_api_error_count counter",
        f"fraudshield_api_error_count {ObservabilityMetrics.api_error_count}",
        "# HELP fraudshield_prediction_count Total model predictions.",
        "# TYPE fraudshield_prediction_count counter",
        f"fraudshield_prediction_count {ObservabilityMetrics.prediction_count}",
        "# HELP fraudshield_prediction_latency_seconds Average prediction latency.",
        "# TYPE fraudshield_prediction_latency_seconds gauge",
        f"fraudshield_prediction_latency_seconds {ObservabilityMetrics.average_prediction_latency():.6f}",
        "# HELP fraudshield_fraud_rate Ratio of predictions flagged as fraud.",
        "# TYPE fraudshield_fraud_rate gauge",
        f"fraudshield_fraud_rate {ObservabilityMetrics.fraud_rate():.6f}",
        "# HELP fraudshield_prediction_throughput_per_second Prediction throughput.",
        "# TYPE fraudshield_prediction_throughput_per_second gauge",
        f"fraudshield_prediction_throughput_per_second {ObservabilityMetrics.throughput_per_second():.6f}",
        "# HELP fraudshield_model_precision Latest measured model precision.",
        "# TYPE fraudshield_model_precision gauge",
        f"fraudshield_model_precision {ObservabilityMetrics.model_precision:.6f}",
        "# HELP fraudshield_model_recall Latest measured model recall.",
        "# TYPE fraudshield_model_recall gauge",
        f"fraudshield_model_recall {ObservabilityMetrics.model_recall:.6f}",
        "# HELP fraudshield_model_f1 Latest measured model F1.",
        "# TYPE fraudshield_model_f1 gauge",
        f"fraudshield_model_f1 {ObservabilityMetrics.model_f1:.6f}",
        "# HELP fraudshield_model_roc_auc Latest measured model ROC AUC.",
        "# TYPE fraudshield_model_roc_auc gauge",
        f"fraudshield_model_roc_auc {ObservabilityMetrics.model_roc_auc:.6f}",
        "# HELP fraudshield_drift_score Latest feature or prediction drift score.",
        "# TYPE fraudshield_drift_score gauge",
        f"fraudshield_drift_score {ObservabilityMetrics.drift_score:.6f}",
        "# HELP fraudshield_cpu_usage_percent CPU usage percent.",
        "# TYPE fraudshield_cpu_usage_percent gauge",
        f"fraudshield_cpu_usage_percent {snapshot['cpu_usage']}",
        "# HELP fraudshield_memory_usage_percent Memory usage percent.",
        "# TYPE fraudshield_memory_usage_percent gauge",
        f"fraudshield_memory_usage_percent {snapshot['memory_usage']}",
        "# HELP fraudshield_disk_usage_percent Disk usage percent.",
        "# TYPE fraudshield_disk_usage_percent gauge",
        f"fraudshield_disk_usage_percent {snapshot['disk_usage']}",
        "# HELP fraudshield_mongodb_up MongoDB health flag.",
        "# TYPE fraudshield_mongodb_up gauge",
        f"fraudshield_mongodb_up {mongodb_up}",
        "# HELP fraudshield_model_loaded Model loaded flag.",
        "# TYPE fraudshield_model_loaded gauge",
        f"fraudshield_model_loaded {model_loaded}",
        "# HELP fraudshield_model_version Current deployed model version.",
        "# TYPE fraudshield_model_version gauge",
        f'fraudshield_model_version{{version="{settings.MODEL_VERSION}"}} 1',
    ]

    return "\n".join(lines) + "\n"


@router.get("/metrics")
def metrics():
    return Response(
        content=render_prometheus_metrics(),
        media_type="text/plain; version=0.0.4"
    )
