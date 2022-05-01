from flask import Blueprint, send_from_directory, make_response, jsonify, request
import sqlite3

from appmain import app

from appmain.utils import verifyJWT, getJWTContent

article = Blueprint('article', __name__)

@article.route('/create_article')
def createArticlePage():
    return send_from_directory(app.root_path, 'templates/create_article.html')

