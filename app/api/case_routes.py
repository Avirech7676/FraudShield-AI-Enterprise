from fastapi import APIRouter, Depends, HTTPException
from app.services.case_service import CaseService
from app.auth.jwt_dependency import verify_token

router = APIRouter()
case_service = CaseService()


@router.get("/cases")
def get_cases(user=Depends(verify_token)):
    return case_service.get_all_cases()


@router.get("/cases/stats")
def get_case_stats(user=Depends(verify_token)):
    return case_service.get_statistics()


@router.get("/cases/{case_id}")
def get_case(case_id: str, user=Depends(verify_token)):
    case = case_service.get_case(case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case


@router.put("/cases/{case_id}/assign")
def assign_case(case_id: str, data: dict, user=Depends(verify_token)):
    analyst = data.get("assigned_to")
    if not analyst:
        raise HTTPException(status_code=400, detail="assigned_to is required")
    case = case_service.assign_case(case_id, analyst)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case


@router.post("/cases/{case_id}/notes")
def add_case_note(case_id: str, data: dict, user=Depends(verify_token)):
    note = data.get("note")
    if not note:
        raise HTTPException(status_code=400, detail="note is required")
    case = case_service.add_case_note(case_id, note)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case


@router.put("/cases/{case_id}/close")
def close_case(case_id: str, data: dict, user=Depends(verify_token)):
    resolution = data.get("resolution")
    if not resolution:
        raise HTTPException(status_code=400, detail="resolution is required")
    case = case_service.close_case(case_id, resolution)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case


@router.put("/cases/{case_id}/reopen")
def reopen_case(case_id: str, user=Depends(verify_token)):
    case = case_service.reopen_case(case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case
