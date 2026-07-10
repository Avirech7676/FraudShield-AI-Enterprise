import requests

from app.notifications.config import *

class TeamsService:

    @staticmethod
    def send(message):
        if not TEAMS_WEBHOOK:
            raise ValueError("TEAMS_WEBHOOK is not configured")

        response = requests.post(

            TEAMS_WEBHOOK,

            json={

                "text": message

            },

            timeout=10

        )
        response.raise_for_status()
