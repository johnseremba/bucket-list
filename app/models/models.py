from datetime import datetime
from flask_login import login_manager, UserMixin, login_required, login_user, logout_user
from app.routes import db


class User(db.Model, UserMixin):
    def __init__(self, username, email):
        self.username = username
        self.email = email

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True)
    surname = db.Column(db.String(80), nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    gender = db.Column(db.String(10))
    active = db.Column(db.Boolean, default=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    date_modified = db.Column(db.DateTime)

    def __repr__(self):
        return "<User %r>" % self.username


class BucketList(db.Model):
    __tablename__ = "bucketlist"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.Text)
    interests = db.Column(db.String(120))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    date_modified = db.Column(db.DateTime)

    def __repr__(self):
        return "<Bucketlist %r>" % self.name


class Item(db.Model):
    __tablename__ = "item"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bucket_list = db.Column(db.Integer, db.ForeignKey('bucketlist.id'))
    name = db.Column(db.String(100), unique=True)
    category = db.Column(db.String(120))
    location = db.Column(db.String(150))
    description = db.Column(db.Text)
    category = db.Column(db.String(50))
    status = db.Column(db.String(100))
    date_accomplished = db.Column(db.DateTime)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    date_modified = db.Column(db.DateTime)

    def __repr__(self):
        return "<Items %r>" % self.name


class ItemPhotos(db.Model):
    __tablename__ = "images"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    url = db.Column(db.String(200), unique=True)
    caption = db.Column(db.String(150))
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    date_modified = db.Column(db.DateTime)
