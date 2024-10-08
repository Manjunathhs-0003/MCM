from flask_mail import Message
from twilio.rest import Client
from app import mail
from flask import current_app


def send_notification(subject, recipients, body, sender=None):
    sender_email = sender or current_app.config.get('MAIL_DEFAULT_SENDER')
    if not sender_email:
        raise ValueError("No sender email is defined.")
    msg = Message(subject, recipients=recipients, body=body, sender=sender_email)
    mail.send(msg)


def send_sms(to, body):
    account_sid = current_app.config["TWILIO_ACCOUNT_SID"]
    auth_token = current_app.config["TWILIO_AUTH_TOKEN"]
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=body, from_=current_app.config["TWILIO_PHONE_NUMBER"], to=to
    )
    return message.sid


def send_email(subject, recipients, body):
    print("send_email function called")
    msg = Message(subject, recipients=recipients)
    msg.body = body
    mail.send(msg)


print("notification_utils loaded")
