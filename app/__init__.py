from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import configuration

db = SQLAlchemy()
# auth = HTTPBasicAuth()


def create_app(environment):
    my_app = Flask(__name__)
    my_app.config.from_object(configuration[environment])
    my_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(my_app)
    return my_app
