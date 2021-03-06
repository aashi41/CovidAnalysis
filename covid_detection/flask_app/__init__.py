from flask import Flask
from flask_app.config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    from flask_app.main.routes import main
    app.register_blueprint(main)

    return app
