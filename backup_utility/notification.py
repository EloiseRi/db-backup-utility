import requests
from .logger import setup_logger

logger = setup_logger(__name__)

def send_slack_notification(webhook_url, message):
    try:
        slack_data = {
            'text': message
        }
        response = requests.post(
            webhook_url, json=slack_data,
            headers={'Content-Type': 'application/json'}
        )

        if response.status_code != 200:
            logger.error(f"Failed to send notification: {response.status_code}, {response.text}")
            raise ValueError(f"Request to Slack returned an error {response.status_code}, the response is:\n{response.text}")
        else:
            logger.info("Notification sent successfully.")
    except Exception as e:
        logger.error(f"An error occurred while sending notification: {e}")
        raise