from flask import (Blueprint, jsonify, request)

mod = Blueprint('api', __name__)

from app.api.v1.models.bucketlist import Item
from app import db
from app.api.v1.bucketlist.views import get_bucketlist
from app.api.v1.auth.views import login_with_token


@mod.route('/<item_id>', methods=['PUT'])
@login_with_token
def update_item(bucketlist_id, item_id):
    item = get_item(bucketlist_id, item_id)

    if not item or not get_bucketlist(bucketlist_id):
        return jsonify({
            'status': 'fail',
            'message': 'Bucketlist item not found'
        }), 404

    data = request.get_json(force=True)
    item.name = data['name']
    item.description = data['description']
    item.status = data['status']
    db.session.add(item)
    db.session.commit()

    return jsonify({
        'status': 'success',
        'message': 'Bucketlist item updated successfully.',
        'data': {
            'name': item.name,
            'description': item.description,
            'status': item.status,
            'item_id': item.id
        }
    }), 200


@mod.route('/<item_id>', methods=['DELETE'])
@login_with_token
def delete_item(bucketlist_id, item_id):
    item = get_item(bucketlist_id, item_id)

    if not item or not get_bucketlist(bucketlist_id):
        return jsonify({
            'status': 'fail',
            'message': 'Bucketlist item not found'
        }), 404

    db.session.delete(item)
    db.session.commit()

    return jsonify({
        'status': 'success',
        'message': 'Bucketlist item deleted successfully.'
    }), 204


@mod.route('/', methods=['POST'])
@login_with_token
def create_item(bucketlist_id):
    data = request.get_json(force=True)
    bucketlist = get_bucketlist(bucketlist_id)

    if not bucketlist:
        return jsonify({
            'status': 'fail',
            'message': 'Bucketlist does not exist.'
        }), 400

    if not data:
        return jsonify({
            'status': 'fail',
            'message': 'Missing required parameters.'
        }), 400

    name = data['name']
    description = data['description']
    status = data['status']

    new_item = Item(name=name, description=description, status=status, bucketlist=bucketlist.id)
    db.session.add(new_item)
    db.session.commit()
    result = {
        'status': 'success',
        'message': 'Bucketlist item created successfully.',
        'item_id': new_item.id
    }
    return jsonify(result), 201


def get_item(bucketlist_id, item_id):
    bucketlist = get_bucketlist(bucketlist_id)
    if bucketlist:
        return Item.query.filter_by(id=item_id, bucketlist=bucketlist_id).first()
    else:
        return None
