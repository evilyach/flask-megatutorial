import logging
import os
from logging.handlers import RotatingFileHandler, SMTPHandler

from flask import Flask


def enable_logging_to_mail(app: Flask) -> None:
    """Enable logging in email messages.

    Args:
        app (Flask): application object
    """

    auth = None
    if app.config["MAIL_USERNAME"] and app.config["MAIL_PASSWORD"]:
        auth = (app.config["MAIL_USERNAME"], app.config["MAIL_PASSWORD"])

    secure = None
    if app.config["MAIL_USE_TLS"]:
        secure = ()

    mail_handler = SMTPHandler(
        mailhost=(app.config["MAIL_SERVER"], app.config["MAIL_PORT"]),
        fromaddr=f"no-reply@{app.config['MAIL_SERVER']}",
        toaddrs=app.config["ADMINS"],
        subject="Microblog Failure",
        credentials=auth,
        secure=secure,
    )
    mail_handler.setLevel(logging.ERROR)

    app.logger.addHandler(mail_handler)


def enable_logging_to_file(app: Flask) -> None:
    """Enable logging in log file.

    Args:
        app (Flask): application object
    """

    if not os.path.exists("logs"):
        os.mkdir("logs")

    file_handler = RotatingFileHandler(
        "logs/microblog.log", maxBytes=10240, backupCount=10
    )
    file_handler.setLevel(logging.INFO)

    app.logger.addHandler(file_handler)
