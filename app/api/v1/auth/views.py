from flask import (Blueprint, jsonify, request)
from functools import wraps

mod = Blueprint('auth', __name__)

from app.api.v1.models.user import User
from app import db


@mod.route('/login', methods=['POST'])
def login_user():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        return jsonify({
            'status': 'fail',
            'message': 'Username and password required.'
        }), 400

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({
            'status': 'fail',
            'message': 'User not found'
        }), 404

    if not user.verify_password(password):
        return jsonify({
            'status': 'fail',
            'message': 'Invalid username or password'
        }), 403

    auth_token = user.generate_auth_token(user.id).decode()
    result = {
        'status': 'success',
        'message': 'User successfully Logged in.',
        'auth_token': auth_token
    }
    return jsonify(result), 200


@mod.route('/register', methods=['POST'])
def register_user():
    surname = request.json.get('surname')
    first_name = request.json.get('first_name')
    email = request.json.get('email')
    username = request.json.get('username')
    password = request.json.get('password')

    if not username and not password:
        return jsonify({
            'status': 'fail',
            'message': 'Missing required parameters'
        }), 400

    if User.query.filter_by(username=username).first() or \
            User.query.filter_by(email=email).first():
        return jsonify({
            'status': 'fail',
            'message': 'User already exists!'
        }), 403

    user = User(surname=surname, first_name=first_name, email=email, username=username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    auth_token = user.generate_auth_token(user.id).decode()
    return jsonify({
        'status': 'success',
        'message': 'User registered successfully.',
        'auth_token': auth_token
        }), 201


@mod.route('/users/')
def get_user():
    users = list(User.query.all())
    if not users:
        return jsonify({
            'status': 'fail',
            'message': 'User not found'
        }), 404
    result = {
        'status': 'success',
        'message': 'Users retrieved successfully'
    }
    for user in users:
        result[user.id] = {
            'surname': user.surname,
            'first_name': user.first_name,
            'email': user.email,
            'username': user.username
        }
    return jsonify(result), 200


def get_current_user_id():
    auth_token = request.headers.get('Authorization')
    response = User.verify_auth_token(auth_token)
    if not isinstance(response, str):
        user = User.query.get(response)
        return user
    else:
        return None


def login_with_token(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_token = request.headers.get('Authorization')
        if auth_token:
            response = User.verify_auth_token(auth_token)
            if not isinstance(response, str) and User.query.filter_by(id=response).first():
                return func(*args, **kwargs)
            return jsonify({
                'status': 'fail',
                'message': response
            }), 401
        return jsonify({
            'status': 'fail',
            'message': 'Provide a valid authentication token'
        }), 401
    return wrapper