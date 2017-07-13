from datetime import datetime
from flask_login import UserMixin
from manage import app
from app import db
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True)
    surname = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10))
    active = db.Column(db.Boolean, default=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    date_modified = db.Column(db.DateTime)
    bucket_list = db.relationship('BucketList', backref='user', lazy='dynamic')

    def __repr__(self):
        return "<User %r>" % self.username

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data['id'])
        return user


class BucketList(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.Text)
    interests = db.Column(db.String(120))
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    date_modified = db.Column(db.DateTime)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    items = db.relationship('Item', backref='bucket_list', lazy='dynamic')

    def __repr__(self):
        return "<Bucketlist %r>" % self.name


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True)
    category = db.Column(db.String(120))
    location = db.Column(db.String(150))
    description = db.Column(db.Text)
    status = db.Column(db.Text)
    date_accomplished = db.Column(db.DateTime)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    date_modified = db.Column(db.DateTime)
    bucket_list = db.Column(db.Integer, db.ForeignKey('bucket_list.id'), nullable=False)

    def __repr__(self):
        return "<Items %r>" % self.name
