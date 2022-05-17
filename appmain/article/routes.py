import os

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

                # SQL = 'SELECT * FROM articles'
                # cursor.execute(SQL)
                # rows = cursor.fetchall()
                # for row in rows:
                #     print(row)

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
        FROM articles ORDER BY articleNo DESC LIMIT 2,6'
        cursor.execute(SQL)
        result = cursor.fetchall()

        cursor.close()
    conn.close()

    recentArticleDics = []

    if len(result) > 0:
        for article in result:
            recentArticleDics.append({"articleNo": article[0], "title": article[2], "desc": article[4]})

        payload = {"success": True, "articles": recentArticleDics}

    return make_response(jsonify(payload), 200)

@article.route('/display_article/<int:articleNo>', methods=['GET'])
def displayArticlePage(articleNo):
    return send_from_directory(app.root_path, 'templates/display_article.html')

def translateCategory(catId):
    category = '미분류'

    if catId == 0:
        category = '인문'
    elif catId == 1:
        category = '사회과학'
    elif catId == 2:
        category = '자연과학'
    elif catId == 3:
        category = '의학'
    elif catId == 4:
        category = '경제/경영'
    elif catId == 5:
        category = '공학'
    elif catId == 6:
        category = '음악'
    elif catId == 7:
        category = '미술'
    elif catId == 8:
        category = '기타'
    else:
        category = '미분류'

    return category

@article.route('/api/article/display', methods=['GET', 'POST'])
def displayArticle():

    data = request.form
    articleNo = data.get("articleNo")

    payload = {"success": False}

    conn = sqlite3.connect('pyBook.db')
    cursor = conn.cursor()

    if cursor:
        SQL = 'SELECT author, title, category, description, price, picture FROM articles WHERE articleNo=?'
        cursor.execute(SQL, (articleNo,))
        result = cursor.fetchone()

        cursor.close()
    conn.close()

    if result:
        if result[5]:
            picFilePath = 'pics/' + result[0] + '/' + result[5]
            picURL = url_for('static', filename=picFilePath, _external=True)
        else:
            picURL = None

        article = {"author": result[0], "title": result[1], "category": translateCategory(result[2]),
                   "description": result[3], "price": result[4], "picture": picURL}
        payload = {"success": True, "article": article}
    else:
        payload = {"success": True, "article": None}

    return make_response(jsonify(payload), 200)

@article.route('/update_article/<int:articleNo>', methods=['GET'])
def updateArticlePage(articleNo):
    return send_from_directory(app.root_path, 'templates/update_article.html')

@article.route('/api/article/update', methods=['POST'])
def updateArticle():
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

            articleNo = data.get("articleNo")
            category = data.get("category")
            title = data.get("title")
            desc = data.get("desc")
            price = data.get("price")

            conn = sqlite3.connect('pyBook.db')
            cursor = conn.cursor()

            if cursor:
                SQL = 'SELECT author FROM articles WHERE articleNo=?'
                cursor.execute(SQL, (articleNo,))
                result = cursor.fetchone()
                cursor.close()
            conn.close()

            if(result[0] == username):
                if files:
                    conn = sqlite3.connect('pyBook.db')
                    cursor = conn.cursor()

                    if cursor:
                        SQL = 'SELECT picture FROM articles WHERE articleNo=?'
                        cursor.execute(SQL, (articleNo,))
                        result = cursor.fetchone()

                        if result:
                            oldPicFileName = result[0]
                            oldPicFilePath = os.path.join(app.static_folder, 'pics', username, oldPicFileName)

                            if os.path.isfile(oldPicFilePath):
                                os.remove(oldPicFilePath)

                        newPicFileName = savePic(files["picture"], username)

                        SQL = 'UPDATE articles SET category=?, title=?, description=?, picture=?, price=? WHERE articleNo=?'
                        cursor.execute(SQL, (category, title, desc, newPicFileName, price, articleNo))
                        conn.commit()

                        # SQL = 'SELECT * FROM articles'
                        # cursor.execute(SQL)
                        # rows = cursor.fetchall()
                        # for row in rows:
                        #     print(row)

                        cursor.close()
                    conn.close()

                    payload = {"success": True, "articleNo": articleNo}
                else:   # if files
                    conn = sqlite3.connect('pyBook.db')
                    cursor = conn.cursor()

                    if cursor:
                        SQL = 'UPDATE articles SET category=?, title=?, description=?, price=? WHERE articleNo=?'
                        cursor.execute(SQL, (category, title, desc, price, articleNo))
                        conn.commit()

                        # SQL = 'SELECT * FROM articles'
                        # cursor.execute(SQL)
                        # rows = cursor.fetchall()
                        # for row in rows:
                        #     print(row)

                        cursor.close()
                    conn.close()
                    payload = {"success": True, "articleNo": articleNo}
            else:   # if(result[0] == username)
                pass
        else:   # if isValid
            pass
    else:   # if authToken
        pass

    return make_response(jsonify(payload), 200)


@article.route('/api/article/delete', methods=['POST'])
def deleteArticle():
    headerData = request.headers
    data = request.form

    authToken = headerData.get("authtoken")

    payload = {"success": False}

    if authToken:
        isValid = verifyJWT(authToken)

        if isValid:
            token = getJWTContent(authToken)
            username = token["username"]

            articleNo = data.get("articleNo")

            conn = sqlite3.connect('pyBook.db')
            cursor = conn.cursor()

            if cursor:
                SQL = 'SELECT author FROM articles WHERE articleNo=?'
                cursor.execute(SQL, (articleNo,))
                result = cursor.fetchone()
                cursor.close()
            conn.close()

            if(result[0] == username):
                conn = sqlite3.connect('pyBook.db')
                cursor = conn.cursor()

                if cursor:
                    SQL = 'DELETE FROM articles WHERE articleNo=?'
                    cursor.execute(SQL, (articleNo,))
                    conn.commit()
                    cursor.close()
                conn.close()

                print('article deleted:%s' % articleNo)
                payload = {"success": True}
            else:   # if(result[0] == username):
                pass
        else:   # if isValid:
            pass
    else:   # if authToken:
        pass

    return  make_response(jsonify(payload), 200);