from flask import Blueprint

mod = Blueprint('api', __name__)

from app.api.models.models import User, BucketList, Item


@mod.route('/test')
def test():
    return '{"result": "Some little test data"}'
