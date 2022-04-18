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

    conn = sqlite3.connect('users.db')

    with conn:
        with conn.cursor() as cursor:
            SQL = 'INSERT INTO users (username, email, passwd) VALUES (?, ?, ?)'
            cursor.execute(SQL, (username, email, hashedPW))
            conn.commit()

            SQL = 'SELECT * FROM users'
            cursor.execute(SQL)
            rows = cursor.fetchall()
            for row in rows:
                print(row)

    payload = {"success": True}
    return make_response(jsonify(payload), 200)
