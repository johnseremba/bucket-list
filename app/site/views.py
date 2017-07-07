from flask import Blueprint

mod = Blueprint('site', __name__)


@mod.route('/')
@mod.route('/homepage')
def homepage():
    return '<h1>Home Page</h1>'
