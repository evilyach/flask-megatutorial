from flask import Flask, request, current_app
from flask_babel import Babel
from flask_babel import lazy_gettext as _l
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from app.log import enable_logging_to_file, enable_logging_to_mail
from config import Config

db = SQLAlchemy()
migrate = Migrate()

babel = Babel()
bootstrap = Bootstrap()
login = LoginManager()
login.login_view = "auth.login"
login.login_message = _l("Please log in to access this page.")
mail = Mail()
moment = Moment()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    babel.init_app(app)
    bootstrap.init_app(app)
    login.init_app(app)
    mail.init_app(app)
    moment.init_app(app)

    from app.auth import auth_bp
    from app.errors import errors_bp
    from app.core import core_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(errors_bp)
    app.register_blueprint(core_bp)

    if not app.debug and not app.testing:
        if app.config["MAIL_SERVER"]:
            enable_logging_to_mail(app)
        enable_logging_to_file(app)

    return app


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(current_app.config["LANGUAGES"])


from app import models
