import requests

from app.notifications.config import *

class TelegramService:

    @staticmethod
    def send(message):

        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

        requests.post(

            url,

            json={

                "chat_id": TELEGRAM_CHAT_ID,

                "text": message

            }

        )