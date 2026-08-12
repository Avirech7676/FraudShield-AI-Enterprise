import requests
from app.config.logging_config import logger
from app.notifications.config import SMS_API_KEY, SMS_SENDER

class SMSService:
    @staticmethod
    def send(message, phone_number="+15550199"):
        logger.info(f"Simulating SMS Alert to {phone_number} from {SMS_SENDER}: {message}")
        if not SMS_API_KEY:
            # Simulated success
            return True
            
        # In a real production system, you would call a provider API here (e.g. Twilio, Infobip)
        try:
            # Simulated Twilio or SMS Gateway call:
            # response = requests.post("https://api.sms-gateway.com/send", json={"to": phone_number, "msg": message, "key": SMS_API_KEY})
            # response.raise_for_status()
            pass
        except Exception as e:
            logger.error(f"Failed to send real SMS: {e}")
            raise
        return True
