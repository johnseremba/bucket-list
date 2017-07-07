import os
from functools import wraps

from flask import Flask, session, flash, url_for
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['WTF_CSRF_ENABLED'] = True

# Database configuration
app.config['SECRETE_KEY'] = 'eBL0S*wmc2mg?.&;R-7=Z@J+fI)4=QQYu`:}qMA#e>3<R9"[VQ<>%b!1?J!jwD,'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////temp/bucketlist_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

# User authentication
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.init_app(app)

from app.views import *
from app.models import *


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('login_page'))

    return wrap