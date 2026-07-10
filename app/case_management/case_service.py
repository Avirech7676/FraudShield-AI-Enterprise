from datetime import datetime


class CaseService:

    @staticmethod
    def assign(case, analyst):

        case["assigned_to"] = analyst

        case["updated_at"] = datetime.utcnow()

        case["timeline"].append(

            {

                "event": f"Assigned to {analyst}",

                "timestamp": datetime.utcnow()

            }

        )

        return case

    @staticmethod
    def add_note(case, note):

        case["notes"].append(

            {

                "note": note,

                "timestamp": datetime.utcnow()

            }

        )

        case["timeline"].append(

            {

                "event": "Note Added",

                "timestamp": datetime.utcnow()

            }

        )

        case["updated_at"] = datetime.utcnow()

        return case

    @staticmethod
    def close_case(case, resolution):

        case["status"] = "CLOSED"

        case["resolution"] = resolution

        case["updated_at"] = datetime.utcnow()

        case["timeline"].append(

            {

                "event": "Case Closed",

                "timestamp": datetime.utcnow()

            }

        )

        return case

    @staticmethod
    def reopen_case(case):

        case["status"] = "OPEN"

        case["updated_at"] = datetime.utcnow()

        case["timeline"].append(

            {

                "event": "Case Reopened",

                "timestamp": datetime.utcnow()

            }

        )

        return case