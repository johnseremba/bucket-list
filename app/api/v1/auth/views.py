from flask import (Blueprint, jsonify, request)
from functools import wraps

mod = Blueprint('auth', __name__)

from app.api.v1.models.user import User
from app import db


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


@mod.route('/login', methods=['POST'])
def login_user():
    """ Login function requires username and password as mandatory variables """

    data = request.get_json(force=True)
    username = data['username']
    password = data['password']

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
        'auth_token': auth_token
    }

    return jsonify(result), 200


@mod.route('/register', methods=['POST'])
def register_user():
    """ Registration function requires surname, firstname, email, username and password as mandatory parameters """
    data = request.get_json(force=True)  # Data passed must be in json format

    if not data or not data['username'] and not data['password']:
        return jsonify({
            'message': 'Missing required parameters.'
        }), 400

    surname = data['surname']
    firstname = data['firstname']
    email = data['email']
    username = data['username']
    password = data['password']

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
        'auth_token': auth_token
        }), 201


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
    for user in users:
        result[user.id] = {
            'surname': user.surname,
            'firstname': user.first_name,
            'email': user.email,
            'username': user.username
        }

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
