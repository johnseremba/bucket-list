import datetime
import jwt
from flask_login import UserMixin
from manage import app
from app import db
from passlib.apps import custom_app_context as pwd_context


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(120), unique=True)
    surname = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    active = db.Column(db.Boolean, default=True)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    date_modified = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    bucketlist = db.relationship('BucketList', backref='user_bucket_list', lazy='dynamic')

    def __init__(self, surname, first_name, email, username):
        self.surname = surname
        self.first_name = first_name
        self.email = email
        self.username = username

    def __repr__(self):
        return "<User %r>" % self.username

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, user_id):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=1200),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def verify_auth_token(auth_token):
        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return "Signature expired, please log in again!"
        except jwt.InvalidTokenError:
            return "Invalid token! Try again."


class BucketList(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.Text, nullable=True)
    interests = db.Column(db.String(120), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    date_modified = db.Column(db.DateTime)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    items = db.relationship('Item', backref='bucket_list_items', lazy='dynamic')

    def __repr__(self):
        return "<Bucketlist %r>" % self.name


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.Text)
    status = db.Column(db.Text)
    date_accomplished = db.Column(db.DateTime)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    date_modified = db.Column(db.DateTime)
    bucketlist = db.Column(db.Integer, db.ForeignKey('bucket_list.id'), nullable=False)

    def __repr__(self):
        return "<Items %r>" % self.name
