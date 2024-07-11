#!/usr/bin/env python3
""" session authentication views module """
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import environ


@app_views.route('/auth_session/login',
                 methods=['POST'], strict_slashes=False)
def login() -> str:
    """ session authentication login handle """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or email == "":
        return jsonify({ "error": "email missing" }), 400
    if not password or password == "":
        return jsonify({ "error": "password missing" }), 400

    users_list = User.search({"email": email})
    if users_list == []:
        return jsonify({ "error": "no user found for this email" }), 404

    if users_list[0].is_valid_password(password):
        from api.v1.app import auth
        session_id = auth.create_session(users_list[0].id)
        res = jsonify(users_list[0].to_json())
        cookie_name = environ.get('SESSION_NAME')
        res.set_cookie(cookie_name, session_id)
        return res

    return jsonify({ "error": "wrong password" }), 401
