from flask import Blueprint, send_from_directory, make_response, jsonify, request
import sqlite3

from appmain import app

from appmain.utils import verifyJWT, getJWTContent

article = Blueprint('article', __name__)

@article.route('/create_article')
def createArticlePage():
    return send_from_directory(app.root_path, 'templates/create_article.html')

@article.route('/api/article/create', methods=['POST'])
def createArticle():

    headerData = request.headers
    data = request.form
    files =request.files

    authToken = headerData.get("authtoken")
    print('createArticle.authtoken', authToken)

    if authToken:
        isValid = verifyJWT(authToken)

        if isValid:
            print('createArticle.isValid:', isValid)
            token = getJWTContent(authToken)
            username = token["username"]

            category = data.get("category")
            title = data.get("title")
            desc = data.get("desc")

            if files:
                print('createArticle.files', files)

            print('createArticle.username', username)
            print('createArticle.category', category)
            print('createArticle.title', title)
            print('createArticle.desc', desc)

            # conn = sqlite3.connect('pyBook.db')
            # cursor = conn.cursor()
            #
            #     if cursor:
        else:
            pass
    else:
        pass

    payload = {"success": False}

    return make_response(jsonify(payload), 200)