from flask import Blueprint

hello = Blueprint('hello', __name__, url_prefix='/')


@hello.route('/')
def helloWorld():
    return 'Hello Wolrd'
