from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.api.config import configuration

db = SQLAlchemy()
# auth = HTTPBasicAuth()


def create_app(environment):
    app = Flask(__name__)
    app.config.from_object(configuration[environment])
    db.init_app(app)

    return app
