from fastapi import APIRouter

from .schemas import (
    AlertCreate,
    AssignAlert,
    UpdateAlertStatus,
)

from .service import (
    create_alert,
    get_alerts,
    get_alert,
    assign_alert,
    update_status,
    delete_alert,
)

router = APIRouter(
    prefix="/alerts",
    tags=["Alerts"],
)


@router.get("")
def list_alerts():

    return get_alerts()


@router.get("/{alert_id}")
def read_alert(alert_id: str):

    return get_alert(alert_id)


@router.post("")
def create(alert: AlertCreate):

    create_alert(alert.model_dump())

    return {

        "message": "Alert Created Successfully"

    }


@router.patch("/{alert_id}/assign")
def assign(alert_id: str, request: AssignAlert):

    assign_alert(

        alert_id,

        request.assigned_to,

    )

    return {

        "message": "Alert Assigned"

    }


@router.patch("/{alert_id}/status")
def update(alert_id: str, request: UpdateAlertStatus):

    update_status(

        alert_id,

        request.status,

    )

    return {

        "message": "Alert Updated"

    }


@router.delete("/{alert_id}")
def delete(alert_id: str):

    delete_alert(alert_id)

    return {

        "message": "Alert Deleted"

    }