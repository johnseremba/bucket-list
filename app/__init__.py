from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import configuration

db = SQLAlchemy()


def create_app(environment):
    my_app = Flask(__name__)
    my_app.config.from_object(configuration[environment])
    my_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(my_app)

    from app.api.v1.item.views import mod as item_views
    from app.api.v1.bucketlist.views import mod as bucketlist_views
    from app.api.v1.auth.views import mod as auth_views

    my_app.register_blueprint(auth_views, url_prefix='/api/v1/auth')
    my_app.register_blueprint(bucketlist_views, url_prefix='/api/v1/bucketlists')
    my_app.register_blueprint(bucketlist_views, url_prefix='/api/v1/bucketlists/<bucketlist_id>/items')

    return my_app
