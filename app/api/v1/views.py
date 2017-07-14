import datetime
from flask import Blueprint, jsonify, request
from werkzeug.exceptions import abort

mod = Blueprint('api', __name__)

from app.api.v1.models.models import User, BucketList, Item
from app import db


@mod.route('/test')
def test():
    return '{"result": "Some little test data"}'


@mod.route('/auth/login', methods=['POST'])
def login_user():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        abort(400)

    user = User.query.filter_by(username=username).first()
    if not user:
        abort(400)
    if not user.verify_password(password):
        abort(400)
    result = {
        'user_id': user.id,
        'surname': user.surname,
        'first_name': user.first_name,
        'email': user.email
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
        abort(400)  # missing arguments
    if User.query.filter_by(username=username).first() or \
            User.query.filter_by(email=email).first():
        abort(400)  # existing user
    user = User(surname=surname, first_name=first_name, email=email, username=username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({
        'username': user.username,
        'first_name': user.first_name,
        'surname': user.username,
        'email': user.email
        }), 201


@mod.route('/auth/users/')
def get_user():
    users = list(User.query.all())
    if not users:
        abort(400)
    result = {}
    for user in users:
        result[user.id] = {
            'surname': user.surname,
            'first_name': user.first_name,
            'email': user.email,
            'username': user.username
        }
    return jsonify(result), 200


@mod.route('/bucketlists/', methods=['POST'])
def create_bucketlist():
    created_by = request.json.get('created_by')
    name = request.json.get('name')
    description = request.json.get('description')
    interests = request.json.get('interests')

    if not created_by or not name:
        abort(400)  # missing required params

    user = User.query.filter_by(id=created_by).first()

    if not user:
        abort(400)  # user doesn't exist

    bucketlist = BucketList(created_by=created_by, name=name, description=description, interests=interests)
    db.session.add(bucketlist)
    db.session.commit()

    result = {
        'id': bucketlist.id,
        'name': bucketlist.name,
        'description': bucketlist.description,
        'interests': bucketlist.interests,
        'items': []
    }

    return jsonify(result), 200


@mod.route('/bucketlists/', defaults={'id': None}, methods=['GET'])
@mod.route('/bucketlists/<id>', methods=['GET', 'PUT'])
def get_all_bucketlists(id):
    if request.method == "PUT":
        bucketlist = BucketList.query.get(id)
        if not bucketlist:
            abort(400)  # Bucketlist not found
        bucketlist.name = request.json.get('name')
        bucketlist.description = request.json.get('description')
        bucketlist.interests = request.json.get('interests')
        bucketlist.date_modified = datetime.datetime.now()
        db.session.add(bucketlist)
        db.session.commit()
        return "Success", 200

    if not id:
        bucketlists = list(BucketList.query.all())
    else:
        bucketlists = list(BucketList.query.filter_by(id=id))

    result = {}
    for bucketlist in bucketlists:
        result[bucketlist.id] = {
            'id': bucketlist.id,
            'name': bucketlist.name,
            'description': bucketlist.description,
            'interests': bucketlist.interests,
            'items': get_bucketlist_items(bucketlist.id),
            'date_created': bucketlist.date_created,
            'date_modified': bucketlist.date_modified,
            'created_by': bucketlist.created_by
        }
    return jsonify(result), 200


@mod.route('/bucketlists/<id>/items/', methods=['POST'])
def create_bucketlist_item(id):
    name = request.json.get('name')
    description = request.json.get('description')
    status = request.json.get('status')

    bucketlist = BucketList.query.filter_by(id=id).first()

    if not bucketlist:
        abort(400)

    if not name:
        abort(400)

    new_item = Item(name=name, description=description, status=status, bucketlist=bucketlist.id)
    db.session.add(new_item)
    db.session.commit()

    result = {
        'id': new_item.id,
        'name': new_item.name,
        'description': new_item.description,
        'status': new_item.status
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
