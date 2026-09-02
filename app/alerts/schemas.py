from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AlertCreate(BaseModel):
    transaction_id: str
    prediction: str
    risk_score: float
    risk_tier: str
    priority: str
    assigned_to: Optional[str] = ""
    status: str = "Open"


class AlertResponse(BaseModel):
    id: Optional[str] = None
    transaction_id: str
    prediction: str
    risk_score: float
    risk_tier: str
    priority: str
    assigned_to: str
    status: str
    created_at: datetime


class AssignAlert(BaseModel):
    assigned_to: str


class UpdateAlertStatus(BaseModel):
    status: str