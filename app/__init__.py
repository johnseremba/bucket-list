import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['WTF_CSRF_ENABLED'] = True

# Database configuration
app.config['SECRETE_KEY'] = 'eBL0S*wmc2mg?.&;R-7=Z@J+fI)4=QQYu`:}qMA#e>3<R9"[VQ<>%b!1?J!jwD,'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'bucket_list_db')
db = SQLAlchemy(app)
