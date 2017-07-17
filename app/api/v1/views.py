import datetime
from flask import (Blueprint, jsonify, request)
from functools import wraps

mod = Blueprint('api', __name__)

from app.api.v1.models.models import User, BucketList, Item
from app import db


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


@mod.route('/auth/login', methods=['POST'])
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


@mod.route('/auth/register', methods=['POST'])
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


@mod.route('/auth/users/')
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


@mod.route('/bucketlists/', methods=['POST'])
@login_with_token
def create_bucketlist():
    created_by = request.json.get('created_by')
    name = request.json.get('name')
    description = request.json.get('description')
    interests = request.json.get('interests')

    if not created_by or not name:
        return jsonify({
            'status': 'fail',
            'message': 'Missing required parameters'
        }), 400

    user = User.query.filter_by(id=created_by).first()

    if not user:
        return jsonify({
            'status': 'fail',
            'message': 'User does not exist'
        }), 404

    bucketlist = BucketList(created_by=created_by, name=name, description=description, interests=interests)
    db.session.add(bucketlist)
    db.session.commit()

    result = {
        'status': 'success',
        'message': 'Bucketlist created successfully',
        'data': {
            'id': bucketlist.id,
            'name': bucketlist.name,
            'description': bucketlist.description,
            'interests': bucketlist.interests,
            'items': []
        }
    }
    return jsonify(result), 200


@mod.route('/bucketlists/', defaults={'id': None}, methods=['GET'])
@mod.route('/bucketlists/<id>', methods=['GET', 'PUT', 'DELETE'])
@login_with_token
def bucketlists(id):
    if request.method == "PUT":
        bucketlist = get_bucketlist(id)
        if not bucketlist:
            return jsonify({
                'status': 'fail',
                'message': 'Bucketlist not found.'
            }), 404
        bucketlist.name = request.json.get('name')
        bucketlist.description = request.json.get('description')
        bucketlist.interests = request.json.get('interests')
        bucketlist.date_modified = datetime.datetime.now()
        db.session.add(bucketlist)
        db.session.commit()
        return jsonify({
            'status': 'success',
            'message': 'Bucketlist updated successfully'
        }), 200
    elif request.method == "DELETE":
        bucketlist = get_bucketlist(id)

        if not bucketlist:
            return jsonify({
                'status': 'fail',
                'message': 'Bucketlist not found.'
            }), 404

        db.session.delete(bucketlist)
        db.session.commit()
        return jsonify({
            'status': 'success',
            'message': 'Bucketlist deleted successfully.'
        }), 200
    elif request.method == "GET":
        auth_token = request.headers.get('Authorization')
        response = User.verify_auth_token(auth_token)
        if not isinstance(response, str):
            user = User.query.get(response)
        if not id:
            bucketlists = list(BucketList.query.filter_by(created_by=user.id))
        else:
            bucketlists = list(BucketList.query.filter_by(created_by=user.id, id=id))
        result = {}
        for bucketlist in bucketlists:
            result[bucketlist.name] = {
                'description': bucketlist.description,
                'interests': bucketlist.interests,
                'items': get_bucketlist_items(bucketlist.id),
                'date_created': bucketlist.date_created,
                'date_modified': bucketlist.date_modified,
                'created_by': bucketlist.created_by,
                'id': bucketlist.id
            }
        response = {
            'message': 'Bucketlists retrieved successfully.',
            'status': 'success',
            'data': result
        }
        return jsonify(response), 200


@mod.route('/bucketlists/<id>/items/', defaults={'item_id': None}, methods=['POST'])
@mod.route('/bucketlists/<id>/items/<item_id>', methods=['PUT', 'DELETE'])
@login_with_token
def crud_bucketlist_item(id, item_id):
    if request.method == "PUT":
        item = get_item(item_id)

        if not item or not get_bucketlist(id):
            return jsonify({
                'status': 'fail',
                'message': 'Bucketlist item not found'
            }), 404

        item.name = request.json.get('name')
        item.description = request.json.get('description')
        item.status = request.json.get('status')
        db.session.add(item)
        db.session.commit()
        return jsonify({
            'status': 'success',
            'message': 'Bucketlist item updated successfully.'
        }), 200
    elif request.method == "DELETE":
        item = get_item(id)
        db.session.delete(item)
        db.session.commit()
        return jsonify({
            'status': 'success',
            'message': 'Bucketlist item deleted successfully.'
        }), 200
    elif request.method == "POST":
        name = request.json.get('name')
        description = request.json.get('description')
        status = request.json.get('status')
        bucketlist = get_bucketlist(id)

        if not bucketlist:
            return jsonify({
                'status': 'fail',
                'message': 'Bucketlist does not exist.'
            }), 400

        if not name:
            return jsonify({
                'status': 'fail',
                'message': 'missing required parameters.'
            }), 400

        new_item = Item(name=name, description=description, status=status, bucketlist=bucketlist.id)
        db.session.add(new_item)
        db.session.commit()
        result = {
            'status': 'success',
            'message': 'Bucketlist item created successfully!'
        }
        return jsonify(result), 200


def get_bucketlist_items(bucketlist_id):
    items = list(Item.query.filter_by(bucketlist=bucketlist_id))
    result = []
    for item in items:
        result.append({
            'id': item.id,
            'name': item.name,
            'description': item.description,
            'status': item.status,
            'date_accomplished': item.date_accomplished,
            'date_created': item.date_created
        })
    return result


def get_bucketlist(bucketlist_id):
    return BucketList.query.get(bucketlist_id)


def get_item(item_id):
    return Item.query.get(item_id)
