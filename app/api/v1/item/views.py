from flask import (Blueprint, jsonify, request)

mod = Blueprint('api', __name__)

from app.api.v1.models.bucketlist import Item
from app import db
from app.api.v1.bucketlist.views import get_bucketlist
from app.api.v1.auth.views import login_with_token, crossdomain


@crossdomain
@mod.route('/<item_id>', methods=['PUT'])
@login_with_token
def update_item(bucketlist_id, item_id):
    """
    Updates a bucket list item. Takes the bucketlist id as a required parameter.
    :param bucketlist_id:
    :param item_id:
    :return:
    """
    item = get_item(bucketlist_id, item_id)

    if not item or not get_bucketlist(bucketlist_id):
        return jsonify({
            'message': 'Bucketlist item not found.'
        }), 404

    data = request.get_json(force=True)
    name = data.get('name', None)
    description = data.get('description', None)
    status = data.get('status', None)
    date_accomplished = data.get('date_accomplished', None)

    if name:
        item.name = name
    if description:
        item.description = description
    if status:
        item.status = status
    if date_accomplished:
        item.date_accomplished = date_accomplished

    db.session.add(item)
    db.session.commit()

    return jsonify({
        'message': 'Bucketlist item updated successfully.',
        'data': {
            'name': item.name,
            'description': item.description,
            'status': item.status,
            'item_id': item.id
        }
    }), 200


@crossdomain
@mod.route('/<item_id>', methods=['DELETE'])
@login_with_token
def delete_item(bucketlist_id, item_id):
    """
    Deletes a bucketlist item
    :param bucketlist_id:
    :param item_id:
    :return:
    """
    item = get_item(bucketlist_id, item_id)

    if not item or not get_bucketlist(bucketlist_id):
        return jsonify({
            'message': 'Bucketlist item not found.'
        }), 404

    db.session.delete(item)
    db.session.commit()

    return jsonify({
        'message': 'Bucketlist item deleted successfully.'
    }), 202


@crossdomain
@mod.route('/', methods=['POST'])
@login_with_token
def create_item(bucketlist_id):
    """
    Creates a new item for a bucketlist
    :param bucketlist_id:
    :return:
    """
    data = request.get_json(force=True)
    bucketlist = get_bucketlist(bucketlist_id)

    if not bucketlist:
        return jsonify({
            'message': 'Bucketlist does not exist.'
        }), 400

    name = data.get('name', None)
    description = data.get('description', None)
    status = data.get('status', None)

    if not name or not description or not status:
        return jsonify({
            'message': 'Missing required parameters.'
        }), 400

    new_item = Item(name=name, description=description, status=status, bucketlists=bucketlist.id)
    db.session.add(new_item)
    db.session.commit()
    result = {
        'message': 'Bucketlist item created successfully.',
        'data': {
            'id': new_item.id,
            'name': new_item.name,
            'description': new_item.description,
            'status': new_item.status
        }
    }
    return jsonify(result), 201


def get_item(bucketlist_id, item_id):
    """
    Get an individual bucketlist item given the id
    :param bucketlist_id:
    :param item_id:
    :return:
    """
    bucketlist = get_bucketlist(bucketlist_id)
    if bucketlist:
        return Item.query.filter_by(id=item_id, bucketlists=bucketlist_id).first()
    else:
        return None
