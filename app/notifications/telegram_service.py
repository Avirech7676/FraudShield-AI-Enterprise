import requests

from app.notifications.config import *

class TelegramService:

    @staticmethod
    def send(message):
        if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
            raise ValueError("Telegram credentials are not configured")

        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

        response = requests.post(

            url,

            json={

                "chat_id": TELEGRAM_CHAT_ID,

                "text": message

            },

            timeout=10

        )
        response.raise_for_status()
