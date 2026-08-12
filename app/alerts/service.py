from datetime import datetime

from bson import ObjectId

from .models import alerts_collection


def create_alert(data: dict):

    data["created_at"] = datetime.utcnow()

    result = alerts_collection.insert_one(data)

    return str(result.inserted_id)


def get_alerts():

    alerts = []

    for alert in alerts_collection.find():

        alert["_id"] = str(alert["_id"])

        alerts.append(alert)

    return alerts


def get_alert(alert_id):

    alert = alerts_collection.find_one(
        {"_id": ObjectId(alert_id)}
    )

    if alert:

        alert["_id"] = str(alert["_id"])

    return alert


def assign_alert(alert_id, analyst):

    alerts_collection.update_one(

        {

            "_id": ObjectId(alert_id)

        },

        {

            "$set": {

                "assigned_to": analyst

            }

        }

    )


def update_status(alert_id, status):

    alerts_collection.update_one(

        {

            "_id": ObjectId(alert_id)

        },

        {

            "$set": {

                "status": status

            }

        }

    )


def delete_alert(alert_id):

    alerts_collection.delete_one(

        {

            "_id": ObjectId(alert_id)

        }

    )