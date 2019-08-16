from twilio.rest import Client

from cfg import CFG


def send_message(message, numbers):
    # Your Account SID from twilio.com/console
    account_sid = CFG.ACCOUNT_SID
    # Your Auth Token from twilio.com/console
    auth_token  = CFG.AUTH_TOKEN

    client = Client(account_sid, auth_token)
    for number in numbers:
        message_to_send = client.messages.create(
            to="+"+number,
            from_="+"+CFG.FROM_NUMBER,
            body=message)
        print(message_to_send.sid)
