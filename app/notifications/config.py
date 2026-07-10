import os
from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER") or os.getenv("EMAIL_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS") or os.getenv("EMAIL_USERNAME")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK")
TEAMS_WEBHOOK = os.getenv("TEAMS_WEBHOOK")

# SMS & Webhooks config
SMS_API_KEY = os.getenv("SMS_API_KEY")
SMS_SENDER = os.getenv("SMS_SENDER", "FraudShield")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
