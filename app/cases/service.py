from datetime import datetime

from bson import ObjectId

from .models import cases_collection


def create_case(data):

    data["created_at"] = datetime.utcnow()

    data["closed_at"] = None

    result = cases_collection.insert_one(data)

    return str(result.inserted_id)


def get_cases():

    result = []

    for case in cases_collection.find():

        case["_id"] = str(case["_id"])

        result.append(case)

    return result


def get_case(case_id):

    case = cases_collection.find_one(

        {

            "case_id": case_id

        }

    )

    if case:

        case["_id"] = str(case["_id"])

    return case


def assign_case(

    case_id,

    analyst

):

    cases_collection.update_one(

        {

            "case_id": case_id

        },

        {

            "$set": {

                "assigned_to": analyst

            }

        }

    )


def update_status(

    case_id,

    status

):

    update = {

        "status": status

    }

    if status == "Closed":

        update["closed_at"] = datetime.utcnow()

    cases_collection.update_one(

        {

            "case_id": case_id

        },

        {

            "$set": update

        }

    )


def update_notes(

    case_id,

    notes

):

    cases_collection.update_one(

        {

            "case_id": case_id

        },

        {

            "$set": {

                "investigation_notes": notes

            }

        }

    )


def delete_case(

    case_id

):

    cases_collection.delete_one(

        {

            "case_id": case_id

        }

    )