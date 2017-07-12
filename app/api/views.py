from flask import Blueprint
from app.api.models.models2 import Result

mod = Blueprint('api', __name__)


@mod.route('/test')
def test():
    return '{"result": "Some little test data"}'

# from flask import render_template, jsonify, g
#
# from app import create_app
# from app.api.forms import LoginForm
# from app.models import User
#
# app = create_app('development')
#
#
# @app.route('/')
# def index():
#     return render_template('index.html')
#
#
# @app.route('/login', methods=["GET", "POST"])
# def login():
#     form = LoginForm()
#     return render_template('login.html', form=form)
#
#
# @app.route('/api/token')
# # @login_required
# def get_auth_token():
#     token = g.user.generate_auth_token()
#     return jsonify({ 'token': token.decode('ascii') })
#
#
# # @auth.verify_password
# def verify_password(username_or_token, password):
#     # first try to authenticate by token
#     user = User.verify_auth_token(username_or_token)
#     if not user:
#         # try to authenticate with username/password
#         user = User.query.filter_by(username = username_or_token).first()
#         if not user or not user.verify_password(password):
#             return False
#     g.user = user
#     return True
#
# if __name__ == "__main__":
#     app.run(debug=True)
