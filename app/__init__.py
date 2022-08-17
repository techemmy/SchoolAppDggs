from flask import Flask
from flask_mail import Mail

from .models import db
from config import config

import os

mail = Mail()


def create_app(config_name=os.getenv('FLASK_CONFIG') or 'default'):
    app = Flask(__name__)
    print("Config", config[config_name])
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    mail.init_app(app)
    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)

    return app
