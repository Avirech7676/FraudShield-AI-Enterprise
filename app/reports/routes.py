from fastapi import APIRouter, Request
from fastapi.responses import Response

from .schemas import ReportRequest
from .service import generate_report, get_reports

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


@router.post("/generate")
def generate_report_endpoint(request: Request, report_request: ReportRequest):
    """
    Generate a report based on the request.
    Can return a file (CSV, Excel, PDF) or JSON.
    """
    db = request.app.state.db
    return generate_report(db, report_request)


@router.get("/history")
def get_report_history():
    """
    Get history of generated reports.
    """
    return get_reports()