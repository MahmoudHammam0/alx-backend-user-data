#!/usr/bin/env python3
""" basic flask app """
from flask import Flask, jsonify, request, abort
from auth import Auth


app = Flask(__name__)
auth = Auth()


@app.route('/', strict_slashes=False)
def home():
    """ home route """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """ register user end point """
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        user = auth.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    return jsonify({"email": f"{email}", "message": "user created"})


@app.route('/sessions', methods=['POST'])
def login() -> str:
    """_summary_

    Returns:
        str: _description_
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not (auth.valid_login(email, password)):
        abort(401)
    else:
        # create a new session
        session_id = auth.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie('session_id', session_id)

    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
