import uuid

from datetime import datetime


class CaseManager:

    @staticmethod
    def create_case(transaction_id, priority):

        return {

            "case_id": str(uuid.uuid4()),

            "transaction_id": transaction_id,

            "priority": priority,

            "status": "OPEN",

            "assigned_to": None,

            "notes": [],

            "evidence": [],

            "timeline": [

                {

                    "event": "Case Created",

                    "timestamp": datetime.utcnow()

                }

            ],

            "resolution": None,

            "created_at": datetime.utcnow(),

            "updated_at": datetime.utcnow()

        }   