from datetime import datetime


class SLATracker:

    @staticmethod
    def hours_open(case):

        created = case["created_at"]

        delta = datetime.utcnow() - created

        return round(

            delta.total_seconds()/3600,

            2

        )

    @staticmethod
    def days_open(case):

        created = case["created_at"]

        delta = datetime.utcnow() - created

        return delta.days

    @staticmethod
    def exceeded(case, hours=24):

        return SLATracker.hours_open(case) >= hours