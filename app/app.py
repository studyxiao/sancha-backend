from flask import Flask
from haw import Haw, Manager

from .api import bp as api_bp
from .view import bp as public_bp


def create_app(config_name: str, static_folder='./upload'):
    app = Flask(__name__, static_folder=static_folder)

    # app.config.from_object(f'app.config.{config_name.capitalize()}Config')
    app.config.from_object('app.config.ProductionConfig')

    app.register_blueprint(api_bp)
    app.register_blueprint(public_bp)
    Haw(app)
    Manager(app)

    return app
