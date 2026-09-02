from fastapi import APIRouter
from .service import *

router = APIRouter(
    tags=["Analytics"]
)

@router.get("/analytics/summary")
def summary():
    return analytics_summary()

@router.get("/analytics/risk-distribution")
def risk():
    return risk_distribution()

@router.get("/analytics/prediction-distribution")
def prediction():
    return prediction_distribution()

@router.get("/analytics/model-performance")
def performance():
    return model_performance()

@router.get("/analytics/fraud-trends")
def trends():
    return fraud_trends()

@router.get("/analytics/country-distribution")
def country():
    return country_distribution()

@router.get("/analytics/merchant-distribution")
def merchant():
    return merchant_distribution()

# Dashboard chart data endpoints
@router.get("/dashboard/bar-chart")
def bar_chart():
    return get_bar_chart_data()

@router.get("/dashboard/area-chart")
def area_chart():
    return get_area_chart_data()

@router.get("/dashboard/radar-chart")
def radar_chart():
    return get_radar_chart_data()

@router.get("/dashboard/treemap")
def treemap():
    return get_treemap_data()