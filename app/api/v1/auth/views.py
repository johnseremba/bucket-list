from datetime import timedelta

from flask import (Blueprint, jsonify, request, current_app, make_response)
from functools import wraps, update_wrapper

from requests.compat import basestring

mod = Blueprint('auth', __name__)

from app.api.v1.models.user import User
from app import db


def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)

    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator


def login_with_token(func):
    """ Decorator function to ensure that methods that require authentication are protected from unauthorized access """

    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_token = request.headers.get('Authorization')
        if auth_token:
            response = User.verify_auth_token(auth_token)
            if not isinstance(response, str) and User.query.filter_by(id=response).first():
                return func(*args, **kwargs)
            return jsonify({
                'message': response
            }), 401
        return jsonify({
            'message': 'Provide a valid authentication token'
        }), 401
    return wrapper


@crossdomain
@mod.route('/login', methods=['POST'])
def login_user():
    """ Login function requires username and password as mandatory variables """

    data = request.get_json(force=True)
    username = data.get('username', None)
    password = data.get('password', None)

    if not username or not password:
        return jsonify({
            'message': 'Username and password required.'
        }), 400

    user = User.query.filter_by(username=username).first()

    if not user or not user.verify_password(password):
        return jsonify({
            'message': 'Invalid username or password'
        }), 403

    auth_token = user.generate_auth_token(user.id).decode()
    result = {
        'message': 'User successfully Logged in.',
        'auth_token': auth_token,
        'data': {
            'id': user.id,
            'username': user.username,
            'firstname': user.first_name,
            'surname': user.surname,
            'email': user.email
        }
    }

    return jsonify(result), 200


@crossdomain
@mod.route('/register', methods=['POST'])
def register_user():
    """ Registration function requires surname, firstname, email, username and password as mandatory parameters """
    data = request.get_json(force=True)  # Data passed must be in json format

    surname = data.get('surname', None)
    firstname = data.get('firstname', None)
    email = data.get('email', None)
    username = data.get('username', None)
    password = data.get('password', None)

    if not surname or not firstname or not email or not username or not password:
        return jsonify({
            'message': 'Missing required parameters.'
        }), 400

    if User.query.filter_by(username=username).first() or \
            User.query.filter_by(email=email).first():
        return jsonify({
            'message': 'User already exists!'
        }), 403

    user = User(surname=surname, first_name=firstname, email=email, username=username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    auth_token = user.generate_auth_token(user.id).decode()

    return jsonify({
        'message': 'User registered successfully.',
        'auth_token': auth_token,
        'data': {
            'id': user.id,
            'surname': user.surname,
            'firstname': user.first_name,
            'username': user.username,
            'email': user.email
        }
        }), 201


@crossdomain
@mod.route('/users/')
def get_user():
    """ Retrieve a list of all users in the system """
    users = list(User.query.all())
    if not users:
        return jsonify({
            'message': 'User not found'
        }), 404
    result = {
        'message': 'Users retrieved successfully'
    }
    data = []
    for user in users:
        data.append({
            'id': user.id,
            'surname': user.surname,
            'firstname': user.first_name,
            'email': user.email,
            'username': user.username
        })
    result['data'] = data
    return jsonify(result), 200


def get_current_user_id():
    """ After the auth_token is verified, a user id is returned which is used to query for the user object"""
    auth_token = request.headers.get('Authorization')
    response = User.verify_auth_token(auth_token)
    if not isinstance(response, str):
        user = User.query.get(response)
        return user
    else:
        return None
