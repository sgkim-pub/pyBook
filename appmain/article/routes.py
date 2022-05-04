from flask import Blueprint, send_from_directory, make_response, jsonify, request, url_for
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

@article.route('/api/article/recent', methods=['GET'])
def getRecentArticles():

    payload = {"success": False}

    conn = sqlite3.connect('pyBook.db')
    cursor = conn.cursor()

    if cursor:
        SQL = 'SELECT articleNo, author, title, category, description, price, picture \
        FROM articles ORDER BY articleNo DESC LIMIT 6'
        cursor.execute(SQL)
        recentArticleTuples = cursor.fetchall()

        cursor.close()
    conn.close()

    print('getRecentArticles().recentArticleTuples:', recentArticleTuples)

    recentArticleDics = []

    if len(recentArticleTuples) > 0:
        for article in recentArticleTuples:
            # if article[6]:
            #     picFilePath = 'pics/' + article[1] + '/' + article[6]
            #     picURL = url_for('static', filename=picFilePath, _external=True)
            # else:
            #     picURL = None
            #
            # recentArticleDics.append({"articleNo": article[0], "author": article[1], "title": article[2],
            #                           "category": article[3], "desc": article[4], "price": article[5],
            #                           "picURL": picURL})

            recentArticleDics.append({"articleNo": article[0], "title": article[2], "desc": article[4]})

        payload = {"success": True, "articles": recentArticleDics}

    return make_response(jsonify(payload), 200)
