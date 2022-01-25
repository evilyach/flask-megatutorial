from cgitb import text
from flask_mail import Message

from app import mail


def send_email(
    subject: str,
    sender: str,
    recipients: str,
    text_body: str,
    html_body: str,
) -> None:
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body

    mail.send()
