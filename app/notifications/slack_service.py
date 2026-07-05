import requests

from app.notifications.config import *

class SlackService:

    @staticmethod
    def send(message):

        requests.post(

            SLACK_WEBHOOK,

            json={

                "text": message

            }

        )