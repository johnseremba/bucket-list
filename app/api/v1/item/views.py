from flask import (Blueprint, jsonify, request, url_for)

mod = Blueprint('api', __name__)

from app.api.v1.models.bucketlist import Item
from app import db
from app.api.v1.bucketlist.views import get_bucketlist
from app.api.v1.auth.views import login_with_token


@mod.route('/', defaults={'item_id': None}, methods=['POST'])
@mod.route('/<item_id>', methods=['PUT', 'DELETE'])
@login_with_token
def crud_bucketlist_item(bucketlist_id, item_id):
    if request.method == "PUT":
        item = get_item(item_id)

        if not item or not get_bucketlist(bucketlist_id):
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
        item = get_item(bucketlist_id)
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
        bucketlist = get_bucketlist(bucketlist_id)

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
        return jsonify(result), 201


def get_item(item_id):
    return Item.query.get(item_id)