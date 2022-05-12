from flask import Blueprint, request, make_response

import sqlite3

from appmain import app

from appmain.utils import verifyJWT, getJWTContent

reply = Blueprint('reply', __name__)

@reply.route('/api/reply/leave')
def leaveReply():
    headerData = request.headers
    data = request.form

    authToken = headerData.get("authtoken")

    payload = {"success": False}

    if authToken:
        isValid = verifyJWT(authToken)

        if isValid:
            token = getJWTContent(authToken)
            username = token["username"]
        else:   # if isValid:
            pass
    else:   # if authToken:
        pass
    