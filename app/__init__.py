from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.api.views import mod
from app.config import configuration
from app.site.views import mod

db = SQLAlchemy()
# auth = HTTPBasicAuth()


def create_app(environment):
    my_app = Flask(__name__)
    my_app.config.from_object(configuration[environment])
    db.init_app(my_app)
    my_app.register_blueprint(site.views.mod)
    my_app.register_blueprint(api.views.mod, url_prefix='/api')

    return my_app
