from datetime import datetime


class EscalationEngine:

    @staticmethod
    def escalate(case):

        case["status"] = "ESCALATED"

        case["timeline"].append(

            {

                "event": "Case Escalated",

                "timestamp": datetime.utcnow()

            }

        )

        case["updated_at"] = datetime.utcnow()

        return case

    @staticmethod
    def auto_escalate(case):

        if (

            case["priority"] == "P1"

            and

            case["assigned_to"] is None

        ):

            return True

        return False
