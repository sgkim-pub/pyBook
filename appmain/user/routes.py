from flask import Blueprint, send_from_directory, make_response, jsonify, request
import sqlite3
import bcrypt
import secrets
import jwt

from appmain import app

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

        SQL = 'SELECT * FROM users'
        cursor.execute(SQL)
        rows = cursor.fetchall()
        for row in rows:
            print(row)

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

        cursor.close()
        conn.close()

        token = jwt.encode({"id": id, "email": email, "username": username, "authkey": authkey},
                           app.config["SECRET_KEY"], algorithm='HS256')
        payload = {"authenticated": True, "email": email, "username": username, "authtoken": token}

        print('user.signin: %s' % email)
    else:
        pass

    response = make_response(jsonify(payload), 200)
    return response
