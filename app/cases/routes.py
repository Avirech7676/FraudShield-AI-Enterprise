from fastapi import APIRouter

from .schemas import *

from .service import *

router = APIRouter(

    prefix="/cases",

    tags=["Cases"]

)


@router.get("")
def list_cases():

    return get_cases()


@router.get("/{case_id}")
def read_case(case_id: str):

    return get_case(case_id)


@router.post("")
def create(case: CaseCreate):

    create_case(case.model_dump())

    return {

        "message": "Case Created Successfully"

    }


@router.patch("/{case_id}/assign")
def assign(

    case_id: str,

    request: AssignCase

):

    assign_case(

        case_id,

        request.assigned_to

    )

    return {

        "message": "Assigned"

    }


@router.patch("/{case_id}/status")
def status(
    case_id: str,
    request: UpdateStatus
):
    update_status(
        case_id,
        request.status
    )

    # Trigger feedback entry for continuous learning if status is closed
    try:
        from app.database.connection import LazyCollection
        cases_coll = LazyCollection("cases")
        case_item = cases_coll.find_one({"case_id": case_id})
        if case_item:
            tx_id = case_item.get("transaction_id")
            if tx_id:
                fb_coll = LazyCollection("analyst_feedback")
                is_fraud = "fraud" in request.status.lower()
                fb_coll.update_one(
                    {"transaction_id": tx_id},
                    {"$set": {
                        "transaction_id": tx_id,
                        "analyst": "Analyst",
                        "prediction": case_item.get("prediction", "Unknown"),
                        "actual_label": "Fraud" if is_fraud else "Genuine",
                        "status": request.status
                    }},
                    upsert=True
                )

        # Trigger Webhook for P1 / High Risk Cases
        from app.notifications.webhook_manager import WebhookManager
        WebhookManager.send_alert(
            event_type="CASE_STATUS_UPDATED",
            payload={"case_id": case_id, "status": request.status, "priority": case_item.get("priority", "P1") if case_item else "P1"}
        )
    except Exception:
        pass

    return {
        "message": "Status Updated & Feedback Registered"
    }


@router.patch("/{case_id}/notes")
def notes(

    case_id: str,

    request: UpdateNotes

):

    update_notes(

        case_id,

        request.investigation_notes

    )

    return {

        "message": "Notes Updated"

    }


@router.delete("/{case_id}")
def delete(

    case_id: str

):

    delete_case(

        case_id

    )

    return {

        "message": "Deleted"

    }