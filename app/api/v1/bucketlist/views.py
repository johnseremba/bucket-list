from flask import (Blueprint, jsonify, request)

mod = Blueprint('bucketlist', __name__)

import datetime
from math import ceil
from sqlalchemy import desc
from app import db
from app.api.v1.models.bucketlist import (BucketList, Item)
from app.api.v1.auth.views import login_with_token, get_current_user_id


@mod.route('/', methods=['POST'])
@login_with_token
def create_bucketlist():
    created_by = get_current_user_id().id
    name = request.json.get('name')
    description = request.json.get('description')
    interests = request.json.get('interests')

    if not created_by or not name:
        return jsonify({
            'status': 'fail',
            'message': 'Missing required parameters'
        }), 400

    if not created_by:
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
    return jsonify(result), 201


@mod.route('/', defaults={'id': None}, methods=['GET'])
@mod.route('/<id>', methods=['GET', 'PUT', 'DELETE'])
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
        user = get_current_user_id()
        result = {}
        if not id:
            bucketlists = BucketList.query.filter_by(created_by=user.id).order_by(desc(BucketList.date_created))
            counted = bucketlists.count()
            start = request.args.get('start')
            limit = request.args.get('limit')

            limit = int(limit) if limit else 20
            start = int(start) if start else 0
            total_pages = ceil(counted / int(limit))
            current_page = find_page(total_pages, limit, start)
            if not current_page:
                return jsonify({
                    'status': 'fail',
                    'message': 'invalid limit or offset value'
                }), 400

            base_url = request.url.rsplit("?", 2)[0] + '?limit={0}'.format(limit)

            if current_page < total_pages:
                new_start = (current_page * limit) + 1
                next_start = new_start if new_start <= counted else counted
                result['next'] = base_url + '&start={0}'.format(next_start)

            if current_page > 1:
                new_start = (start - limit)
                prev_start = new_start if new_start > 1 else 0
                result['prev'] = base_url + '&start={0}'.format(prev_start)

            result['total_pages'] = total_pages
            result['num_results'] = counted
            result['page'] = current_page

            ls = bucketlists.limit(limit).offset(start)
            bucketlists = list(ls)
        else:
            bucketlists = list(BucketList.query.filter_by(created_by=user.id, id=id))

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


def get_bucketlist(bucketlist_id):
    return BucketList.query.get(bucketlist_id)


def find_page(pages, limit, value):
    page_range = [limit * page for page in range(1, pages + 1)]
    for index, my_range in enumerate(page_range):
        if value <= my_range:
            return index + 1
    return None


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
