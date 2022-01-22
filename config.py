import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-shall-never-guess-this"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI") or \
        f"sqlite:///{os.path.join(basedir, 'app.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
