from flask import Flask, render_template, jsonify, g
from flask_sqlalchemy import SQLAlchemy
from requests import auth

# from app import login_required
from app.forms import LoginForm
from app.models import User


def create_app():
    return Flask(__name__)

app = create_app()
db = SQLAlchemy(app)


@app.route('/')
def index():
    # admin = User('admin', 'admin@example.com')
    # db.session.add(admin)
    # db.session.commit()
    return render_template('index.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    return render_template('login.html', form=form)


@app.route('/api/token')
# @login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({ 'token': token.decode('ascii') })


# @auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username = username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True

if __name__ == "__main__":
    app.run(debug=True)
