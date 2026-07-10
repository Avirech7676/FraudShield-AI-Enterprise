import requests

from app.notifications.config import *

class SlackService:

    @staticmethod
    def send(message):
        if not SLACK_WEBHOOK:
            raise ValueError("SLACK_WEBHOOK is not configured")

        response = requests.post(

            SLACK_WEBHOOK,

            json={

                "text": message

            },

            timeout=10

        )
        response.raise_for_status()
