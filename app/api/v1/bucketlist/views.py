from flask import (Blueprint, jsonify, request)

mod = Blueprint('bucketlist', __name__)

import datetime
from math import ceil
from sqlalchemy import desc
from app import db
from app.api.v1.models.bucketlist import (BucketList, Item)
from app.api.v1.auth.views import (login_with_token, get_current_user_id)


@mod.route('/', methods=['POST'])
@login_with_token
def create_bucketlist():
    """ Create bucketlist object. Required params are name, description and interests """
    created_by = get_current_user_id().id
    data = request.get_json(force=True)

    if not created_by or not data:
        return jsonify({
            'status': 'fail',
            'message': 'Missing required parameters.'
        }), 400

    name = data['name']
    description = data['description']
    interests = data['interests']

    bucketlist = BucketList(created_by=created_by, name=name, description=description, interests=interests)
    db.session.add(bucketlist)
    db.session.commit()

    result = {
        'status': 'success',
        'message': 'Bucketlist created successfully.',
        'data': {
            'id': bucketlist.id,
            'name': bucketlist.name,
            'description': bucketlist.description,
            'interests': bucketlist.interests,
            'items': []
        }
    }
    return jsonify(result), 201


@mod.route('/<id>', methods=['PUT'])
@login_with_token
def update_bucketlist(id):
    """
    Update bucketlist object. A bucketlist id should be passed as part of the url.
    Params to update are; name, description and interests
    """
    bucketlist = get_bucketlist(id)

    if not bucketlist:
        return jsonify({
            'status': 'fail',
            'message': 'Bucketlist not found.'
        }), 404

    data = request.get_json(force=True)
    bucketlist.name = data['name']
    bucketlist.description = data['description']
    bucketlist.interests = data['interests']
    bucketlist.date_modified = datetime.datetime.now()
    db.session.add(bucketlist)
    db.session.commit()

    return jsonify({
        'status': 'success',
        'message': 'Bucketlist updated successfully.'
    }), 200


@mod.route('/<id>', methods=['DELETE'])
@login_with_token
def delete_bucketlist(id):
    """ Deletes a bucketlist object given the id """
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
    }), 202


@mod.route('/', defaults={'id': None}, methods=['GET'])
@mod.route('/<id>', methods=['GET'])
@login_with_token
def bucketlists(id):
    """
    Retrieves an individual bucketlist with its items given the id param.
    Otherwise, it returns all bucketlists belonging to the currently logged in user.
    The result is paginated with 20 bucketlists as the default and 100 max
    :param id:
    :return:
    """
    result = {}
    search_param = request.args.get("q")

    if search_param:
        bucketlists = get_bucketlists(param=search_param)
    else:
        if id:
            bucketlists = get_bucketlists(id=id)
        else:
            bucketlists = get_bucketlists()

    if not list(bucketlists):
        return jsonify({
            'status': 'fail',
            'message': 'No bucketlist(s) found.'
        }), 404

    counted = bucketlists.count()
    offset = request.args.get("offset")
    limit = request.args.get("limit")

    limit = int(limit) if limit and limit <= 100 else 20
    offset = int(offset) if offset else 0
    pagination_result = paginate_data(counted, limit, offset)
    bucketlists = list(bucketlists.limit(limit).offset(offset))

    response = {
        'status': 'success',
        'message': 'Bucketlist(s) retrieved successfully.',
        'pagination': pagination_result if pagination_result else {},
        'data': result
    }
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
    return jsonify(response), 200


def paginate_data(counted, limit, offset):
    """
    Custom pagination function.
    :param counted:
    :param limit:
    :param offset:
    :return: {}
    """
    total_pages = ceil(counted / int(limit))
    current_page = find_page(total_pages, limit, offset)

    if not current_page:
        return None

    base_url = request.url.rsplit("?", 2)[0] + '?limit={0}'.format(limit)
    result = {}

    if current_page < total_pages:
        new_start = (current_page * limit) + 1
        next_start = new_start if new_start <= counted else counted
        result['next'] = base_url + '&offset={0}'.format(next_start)

    if current_page > 1:
        new_start = (offset - limit)
        prev_start = new_start if new_start > 1 else 0
        result['prev'] = base_url + '&offset={0}'.format(prev_start)

    result['total_pages'] = total_pages
    result['num_results'] = counted
    result['page'] = current_page

    return result


def get_bucketlist(bucketlist_id):
    """
    Gets a bucketlist object given the id.
    :param bucketlist_id:
    :return:
    """
    user = get_current_user_id()
    return BucketList.query.filter_by(created_by=user.id, id=bucketlist_id).first()


def find_page(pages, limit, value):
    """
    Function to calculate and return the current page of a paginated result.
    :param pages:
    :param limit:
    :param value:
    :return:
    """
    page_range = [limit * page for page in range(1, pages + 1)]
    for index, my_range in enumerate(page_range):
        if value <= my_range:
            return index + 1
    return None


def get_bucketlist_items(bucketlist_id):
    """
    Returns items belonging to a particular bucketlist, given the bucketlist id.
    :param bucketlist_id:
    :return:
    """
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


def get_bucketlists(**kwargs):
    """
    Searches and returns a bucket list object given its id or a search parameter
    :param kwargs:
    :return:
    """
    user = get_current_user_id()
    id = kwargs['id'] if 'id' in kwargs else None
    param = kwargs['param'] if 'param' in kwargs else None

    if param:
        return BucketList.query.filter(BucketList.name.like("%{}%".format(param))).\
            filter(BucketList.created_by == user.id).order_by(desc(BucketList.date_created))

    if id:
        return BucketList.query.filter_by(id=id, created_by=user.id).order_by(desc(BucketList.date_created))
    else:
        return BucketList.query.filter_by(created_by=user.id).order_by(desc(BucketList.date_created))
