import json
import requests
from app.config.logging_config import logger

class WebhookManager:
    """
    Webhook Alert Dispatcher for Slack, PagerDuty, and Custom Enterprise Webhooks.
    """
    @staticmethod
    def send_alert(event_type: str, payload: dict, webhook_url: str = None):
        if not webhook_url:
            logger.info(f"Webhook alert trigger: {event_type} - {payload.get('case_id', 'ALERT')}")
            return True

        try:
            formatted_payload = {
                "text": f"🚨 *[FraudShield AI Alert]* {event_type.upper()}\n"
                        f"*Case ID:* {payload.get('case_id')}\n"
                        f"*Transaction ID:* {payload.get('transaction_id')}\n"
                        f"*Risk Score:* {payload.get('risk_score')}\n"
                        f"*Priority:* {payload.get('priority')}",
                "event_type": event_type,
                "data": payload
            }
            res = requests.post(webhook_url, json=formatted_payload, timeout=5)
            logger.info(f"Webhook dispatch result: {res.status_code}")
            return res.status_code == 200
        except Exception as e:
            logger.warning(f"Failed to dispatch webhook: {e}")
            return False
