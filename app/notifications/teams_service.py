import requests

from app.notifications.config import *

class TeamsService:

    @staticmethod
    def send(message):

        requests.post(

            TEAMS_WEBHOOK,

            json={

                "text": message

            }

        )