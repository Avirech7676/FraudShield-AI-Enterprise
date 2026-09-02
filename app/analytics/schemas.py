from pydantic import BaseModel
from typing import List


class AnalyticsSummary(BaseModel):
    total_predictions: int
    fraud_cases: int
    genuine_cases: int
    average_risk: float
    critical_alerts: int


class ChartItem(BaseModel):
    label: str
    value: int


class ModelPerformance(BaseModel):
    accuracy: float
    precision: float
    recall: float
    f1_score: float