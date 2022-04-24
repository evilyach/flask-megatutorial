from flask import current_app, render_template
from flask_babel import _

from app.core.email import send_email
from app.models import User


def send_password_reset_email(user: User):
    token = user.get_reset_password_token()

    send_email(
        _("[Microblog] Reset Your Password"),
        sender=current_app.config["ADMINS"][0],
        recipients=[user.email],
        text_body=render_template(
            "email/reset_password.txt",
            user=user,
            token=token,
        ),
        html_body=render_template(
            "email/reset_password.html",
            user=user,
            token=token,
        ),
    )
