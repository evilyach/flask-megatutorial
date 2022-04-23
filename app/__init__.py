from flask import Flask, request
from flask_babel import Babel, lazy_gettext as _l
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from app import core
from app.core import routes

from config import Config


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

bootstrap = Bootstrap(app)
login = LoginManager(app)
login.login_view = "login"
login.login_message = _l("Please log in to access this page.")
mail = Mail(app)
moment = Moment(app)
babel = Babel(app)


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(app.config["LANGUAGES"])

from app.auth import auth_bp
app.register_blueprint(auth_bp, url_prefix='/auth')
from app.errors import errors_bp
app.register_blueprint(errors_bp)
from app.core import core_bp
app.register_blueprint(core_bp, url_prefix='/core')


from app import cli, log, models
