from datetime import datetime


class EvidenceManager:

    @staticmethod
    def add_evidence(

        case,

        filename,

        uploaded_by,

        description

    ):

        evidence = {

            "filename": filename,

            "uploaded_by": uploaded_by,

            "description": description,

            "uploaded_at": datetime.utcnow()

        }

        case["evidence"].append(evidence)

        case["timeline"].append(

            {

                "event": "Evidence Uploaded",

                "timestamp": datetime.utcnow()

            }

        )

        case["updated_at"] = datetime.utcnow()

        return case
