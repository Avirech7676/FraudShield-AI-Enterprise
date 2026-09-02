from datetime import datetime
from typing import Optional, Dict, Any

from pydantic import BaseModel


class ReportRequest(BaseModel):
    report_type: str
    format: Optional[str] = "json"
    filters: Optional[Dict[str, Any]] = None


class ReportResponse(BaseModel):
    id: Optional[str] = None
    report_type: str
    data: Optional[Dict[str, Any]] = None
    summary: Optional[str] = None
    executive_summary: Optional[str] = None
    technical_summary: Optional[str] = None
    compliance_summary: Optional[str] = None
    recommendations: Optional[str] = None
    created_at: datetime