import logging
from logging.handlers import (
    RotatingFileHandler,
    SMTPHandler,
)
import os

from app import app


def enable_logging_to_mail():
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
        secure=secure
    )
    mail_handler.setLevel(logging.ERROR)

    app.logger.addHandler(mail_handler)

def enable_logging_to_file():
    if not os.path.exists("logs"):
        os.mkdir("logs")

    file_handler = RotatingFileHandler(
        "logs/microblog.log",
        maxBytes=10240,
        backupCount=10
    )
    file_handler.setLevel(logging.INFO)
    
    app.logger.addHandler(file_handler)


if not app.debug:
    if app.config["MAIL_SERVER"]:
        enable_logging_to_mail()
    enable_logging_to_file()