import logging

from twilio.rest import Client

from cfg import CFG
logging.basicConfig(filename="griddy.log",
                            filemode='a',
                            format="%(asctime)s:%(levelname)s:%(message)s",
                            datefmt='%Y-%m-%d %H:%M:%S',
                            level=logging.DEBUG)

logger = logging.getLogger(__name__)


def send_message(message, numbers):
    # Your Account SID from twilio.com/console
    account_sid = CFG.ACCOUNT_SID
    # Your Auth Token from twilio.com/console
    auth_token  = CFG.AUTH_TOKEN

    client = Client(account_sid, auth_token)
    for number in numbers:
        try:
            client.messages.create(
                to="+"+number,
                from_="+"+CFG.FROM_NUMBER,
                body=message)
        except Exception as e:
            logger.error(f"Error sending message: {e}")
