from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CaseCreate(BaseModel):

    case_id: str

    transaction_id: str

    alert_id: str

    prediction: str

    risk_score: float

    risk_tier: str

    priority: str

    assigned_to: str = ""

    status: str = "Open"

    investigation_notes: str = ""


class CaseResponse(BaseModel):

    id: Optional[str] = None

    case_id: str

    transaction_id: str

    alert_id: str

    prediction: str

    risk_score: float

    risk_tier: str

    priority: str

    assigned_to: str

    status: str

    investigation_notes: str

    created_at: datetime

    closed_at: Optional[datetime]


class AssignCase(BaseModel):

    assigned_to: str


class UpdateStatus(BaseModel):

    status: str


class UpdateNotes(BaseModel):

    investigation_notes: str