from flask import Blueprint, send_from_directory, make_response, jsonify, request
import sqlite3
import bcrypt
import secrets
import jwt
import secrets
from flask_mail import Message

from appmain import app, mail

from appmain.utils import verifyJWT, getJWTContent

user = Blueprint('user', __name__)

@user.route('/signup')
def signUp():
    return send_from_directory(app.root_path, 'templates/signup.html')

@user.route('/api/user/signup', methods=['POST'])
def register():
    data = request.form

    username = data.get("username")
    email = data.get("email")
    passwd = data.get("passwd")

    hashedPW = bcrypt.hashpw(passwd.encode('utf-8'), bcrypt.gensalt())

    conn = sqlite3.connect('pyBook.db')
    cursor = conn.cursor()

    if cursor:
        SQL = 'INSERT INTO users (username, email, passwd) VALUES (?, ?, ?)'
        cursor.execute(SQL, (username, email, hashedPW))
        conn.commit()

        # SQL = 'SELECT * FROM users'
        # cursor.execute(SQL)
        # rows = cursor.fetchall()
        # for row in rows:
        #     print(row)

        cursor.close()
    conn.close()

    payload = {"success": True}
    return make_response(jsonify(payload), 200)

@user.route('/signin')
def signIn():

    return send_from_directory(app.root_path, 'templates/signin.html')

@user.route('/api/user/signin', methods=['POST'])
def getAuth():
    data = request.form

    email = data.get("email")
    passwd = data.get("passwd")

    conn = sqlite3.connect('pyBook.db')
    cursor = conn.cursor()

    payload = {"authenticated": False, "email": '', "username": '', "authtoken": ''}

    if cursor:
        SQL = 'SELECT id, username, passwd FROM users WHERE email=?'
        cursor.execute(SQL, (email,))
        result = cursor.fetchone()

        if result:
            pwMatch = bcrypt.checkpw(passwd.encode('utf-8'), result[2])
            id = result[0]
            username = result[1]
        else:
            pwMatch = None

        if pwMatch:
            authkey = secrets.token_hex(16)

            SQL = 'UPDATE users SET authkey=? WHERE id=?'
            cursor.execute(SQL, (authkey, id))
            conn.commit()

            token = jwt.encode({"id": id, "email": email, "username": username, "authkey": authkey},
                               app.config["SECRET_KEY"], algorithm='HS256')
            payload = {"authenticated": True, "email": email, "username": username, "authtoken": token}

            # print('user.signin: %s' % email)
        else:
            pass

        cursor.close()
    conn.close()

    return make_response(jsonify(payload), 200)


@user.route('/myinfo')
def myPage():
    return send_from_directory(app.root_path, 'templates/mypage.html')

@user.route('/api/user/myinfo', methods=['POST'])
def getMyInfo():
    headerData = request.headers

    authToken = headerData.get("authtoken")

    payload = {"success": False}

    if authToken:
        isValid = verifyJWT(authToken)

        if isValid:
            token = getJWTContent(authToken)
            email = token["email"]

            conn = sqlite3.connect('pyBook.db')
            cursor = conn.cursor()

            if cursor:
                SQL = 'SELECT username FROM users WHERE email=?'
                cursor.execute(SQL, (email,))
                username = cursor.fetchone()[0]
                cursor.close()
            conn.close()

            payload = {"success": True, "username": username}

    return make_response(jsonify(payload), 200)


@user.route('/api/user/update', methods=['POST'])
def updateMyInfo():

    headerData = request.headers
    data = request.form

    authToken = headerData.get("authtoken")
    username = data.get("username")
    passwd = data.get("passwd")

    # print('updateMyInfo.authToken:', authToken)

    payload = {"success": False}

    if authToken:
        isValid = verifyJWT(authToken)

        if isValid:
            token = getJWTContent(authToken)
            email = token["email"]

            hashedPW = bcrypt.hashpw(passwd.encode('utf-8'), bcrypt.gensalt())

            conn = sqlite3.connect('pyBook.db')
            cursor = conn.cursor()

            if cursor:
                if passwd:
                    SQL = 'UPDATE users SET username=?, passwd=? WHERE email=?'
                    cursor.execute(SQL, (username, hashedPW, email))
                else:
                    SQL = 'UPDATE users SET username=? WHERE email=?'
                    cursor.execute(SQL, (username, email))
                conn.commit()

                # SQL = 'SELECT * FROM users'
                # cursor.execute(SQL)
                # rows = cursor.fetchall()
                # for row in rows:
                #     print(row)

                cursor.close()
            conn.close()

    return make_response(jsonify(payload), 200)


@user.route('/resetpw')
def resetpw():
    return send_from_directory(app.root_path, 'templates/reset_passwd.html')

@user.route('/api/user/resetpw', methods=['POST'])
def checkAndSendNewPW():

    data = request.form
    email = data.get("email")

    payload = {"success": False}

    conn = sqlite3.connect('pyBook.db')
    cursor = conn.cursor()

    if cursor:
        SQL = 'SELECT id FROM users WHERE email=?'
        cursor.execute(SQL, (email,))
        result = cursor.fetchone()

        if result:
            id = result[0]
            randPW = secrets.token_hex(8)
            hashedPW = bcrypt.hashpw(randPW.encode('utf-8'), bcrypt.gensalt())

            SQL = 'UPDATE users SET passwd=? WHERE id=?'
            cursor.execute(SQL, (hashedPW, id))
            conn.commit()

            cursor.close()
            conn.close()

            msg = Message(subject='임시 비밀번호', sender='noreply@example.com', recipients=[email])
            msg.body = '임시 비밀번호입니다: ' + randPW

            # print('checkAndSendNewPW.msg:', msg)
            # mail.send(msg)

            payload = {"success": True}
        else:
            payload = {"success": False, "message": '등록되어 있지 않은 이메일입니다.'}
    else:
        pass

    return make_response(jsonify(payload), 200)
