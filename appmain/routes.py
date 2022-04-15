from flask import Blueprint, send_from_directory

from appmain import app

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    return send_from_directory(app.root_path, 'templates/index.html')