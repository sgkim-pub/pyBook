from flask import Blueprint, send_from_directory, make_response, jsonify, request
import sqlite3
import bcrypt

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

@user.route('/api/user/signup', methods=['POST'])
def getAuth():
    data = request.form

    email = data.get("email")
    passwd = data.get("passwd")

    conn = pymysql.connect(host='localhost', user=cfg.DB_USER, password=cfg.DB_PASSWORD,
                           db=cfg.DB, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    payload = {"authenticated": False, "email": '', "username": '', "authToken": ''}

    with conn:
        with conn.cursor() as cursor:
            sql = 'SELECT userNo, username, pw FROM users WHERE email=%s'
            cursor.execute(sql, email)
            result = cursor.fetchone()

    if result:
        pwMatch = bcrypt.checkpw(password.encode('utf-8'), result["pw"].encode('utf-8'))
        username = result["username"]
        userNo = result["userNo"]
    else:
        pwMatch = None

    if pwMatch:
        authkey = secrets.token_hex(16)

        conn = pymysql.connect(host='localhost', user=cfg.DB_USER, password=cfg.DB_PASSWORD,
                               db=cfg.DB, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

        with conn:
            with conn.cursor() as cursor:
                sql = 'UPDATE users SET authkey=%s WHERE email=%s'
                cursor.execute(sql, (authkey, email))
                conn.commit()

        token = jwt.encode({"userno": userNo, "email": email, "username": username, "authkey": authkey},
                           app.config["SECRET_KEY"], algorithm='HS256')
        payload = {"authenticated": True, "email": email, "username": username, "authToken": token}

        print('user.signin: %s' % email)

        response = make_response(jsonify(payload), 200)
        return response
    else:
        pass

        response = make_response(jsonify(payload), 200)
        return response

