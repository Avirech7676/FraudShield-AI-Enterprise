from app.database.connection import MongoDBConnection
from app.database.repository import FraudRepository
from app.case_management.case_service import CaseService as LegacyCaseService


class CaseService:
    """
    Case Service Layer
    Orchestrates the lifecycle operations on cases, linking case management helpers
    to persistent DB storage.
    """

    def __init__(self):
        self.db = MongoDBConnection().connect()
        self.repository = FraudRepository(self.db)

    def get_all_cases(self):
        return self.repository.get_all_cases()

    def get_case(self, case_id):
        return self.repository.get_case(case_id)

    def assign_case(self, case_id, analyst):
        case = self.repository.get_case(case_id)
        if not case:
            return None
        updated_case = LegacyCaseService.assign(case, analyst)
        self.repository.update_case(case_id, {
            "assigned_to": updated_case["assigned_to"],
            "updated_at": updated_case["updated_at"],
            "timeline": updated_case["timeline"]
        })
        return updated_case

    def add_case_note(self, case_id, note):
        case = self.repository.get_case(case_id)
        if not case:
            return None
        updated_case = LegacyCaseService.add_note(case, note)
        self.repository.update_case(case_id, {
            "notes": updated_case["notes"],
            "updated_at": updated_case["updated_at"],
            "timeline": updated_case["timeline"]
        })
        return updated_case

    def close_case(self, case_id, resolution):
        case = self.repository.get_case(case_id)
        if not case:
            return None
        updated_case = LegacyCaseService.close_case(case, resolution)
        self.repository.update_case(case_id, {
            "status": updated_case["status"],
            "resolution": updated_case["resolution"],
            "updated_at": updated_case["updated_at"],
            "timeline": updated_case["timeline"]
        })
        return updated_case

    def reopen_case(self, case_id):
        case = self.repository.get_case(case_id)
        if not case:
            return None
        updated_case = LegacyCaseService.reopen_case(case)
        self.repository.update_case(case_id, {
            "status": updated_case["status"],
            "updated_at": updated_case["updated_at"],
            "timeline": updated_case["timeline"]
        })
        return updated_case

    def get_statistics(self):
        return self.repository.get_case_statistics()
