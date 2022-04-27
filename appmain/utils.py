import jwt
import sqlite3

from appmain import app


def verifyJWT(token):
    if token is None:
        return None
    else:
        try:
            decodedToken = jwt.decode(token, app.config["SECRET_KEY"], algorithms="HS256")
            print('verifyJWT.decodedToken:', decodedToken)
            if decodedToken:
                print('verifyJWT.decodedToken.authkey:', decodedToken["authkey"])
                print('verifyJWT.decodedToken.email:', decodedToken["email"])
                conn = sqlite3.connect('pyBook.db')
                cursor = conn.cursor()

                if cursor:
                    SQL = 'SELECT authkey FROM users WHERE email=?'
                    cursor.execute(SQL, (decodedToken["email"],))
                    authkey = cursor.fetchone()["authkey"]
                    print('verifyJWT.db.authKey:', authkey)
                    cursor.close()

                conn.close()

                # print('verifyJWT.db.authKey:', authkey)

                if authkey == decodedToken["authkey"]:
                    return True
                else:
                    return None
            else:
                return None
        except:
            return None


def getJWTContent(token):
    isVerified = verifyJWT(token)

    if isVerified:
        return jwt.decode(token, app.config["SECRET_KEY"], algorithms="HS256")
    else:
        return None

