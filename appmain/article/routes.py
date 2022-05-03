from flask import Blueprint, send_from_directory, make_response, jsonify, request
import sqlite3

from appmain import app

from appmain.utils import verifyJWT, getJWTContent, savePic

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

    payload = {"success": False}

    if authToken:
        isValid = verifyJWT(authToken)

        if isValid:
            token = getJWTContent(authToken)
            username = token["username"]

            category = data.get("category")
            title = data.get("title")
            desc = data.get("desc")
            price = data.get("price")

            if files:
                # print('createArticle.files', files)
                picFileName = savePic(files["picture"], username)

            # print('createArticle.username', username)
            # print('createArticle.category', category)
            # print('createArticle.title', title)
            # print('createArticle.desc', desc)

            conn = sqlite3.connect('pyBook.db')
            cursor = conn.cursor()

            if cursor:
                if files:
                    SQL = 'INSERT INTO articles (author, title, category, description, price, picture) \
                    VALUES (?, ?, ?, ?, ?, ?)'
                    cursor.execute(SQL, (username, title, category, desc, price, picFileName))
                else:
                    SQL = 'INSERT INTO articles (author, title, category, description, price) \
                    VALUES (?, ?, ?, ?, ?)'
                    cursor.execute(SQL, (username, title, category, desc, price))
                rowId = cursor.lastrowid
                conn.commit()

                # SQL = "PRAGMA table_info(articles)"
                # cursor.execute(SQL)
                # rows = cursor.fetchall()
                # for row in rows:
                #     print(row)

                SQL = 'SELECT * FROM articles'
                cursor.execute(SQL)
                rows = cursor.fetchall()
                for row in rows:
                    print(row)

                cursor.close()
            conn.close()

            payload = {"success": True, "articleNo": rowId}
        else:
            pass
    else:
        pass

    return make_response(jsonify(payload), 200)
