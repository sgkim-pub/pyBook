from flask import Blueprint

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    response = 'pyBook main page'

    return response
