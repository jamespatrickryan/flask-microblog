import logging
from logging.handlers import RotatingFileHandler, SMTPHandler
import os

from flask import Flask, current_app, request

from flask_babel import Babel, lazy_gettext as _l
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from config import Config


babel = Babel()
bootstrap = Bootstrap()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = _l('Please log in to access this page.')
mail = Mail()
migrate = Migrate()
moment = Moment()
db = SQLAlchemy()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    babel.init_app(app)
    bootstrap.init_app(app)
    login.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)

    from app import auth, errors, main

    app.register_blueprint(auth.blueprint, url_prefix='/auth')
    app.register_blueprint(errors.blueprint)
    app.register_blueprint(main.blueprint)

    if not app.debug and not app.testing:
        if app.config['MAIL_SERVER']:
            credentials = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                credentials = app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD']
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@{}'.format(app.config['MAIL_SERVER']),
                toaddrs=app.config['ADMINS'],
                subject='Microblog Failure',
                credentials=credentials,
                secure=secure
            )
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        if not os.path.exists('logs'):
            os.makedirs('logs')
        file_handler = RotatingFileHandler(
            'logs/microblog.log',
            maxBytes=10240,
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Microblog Start-up')

    return app


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])


from app import models
