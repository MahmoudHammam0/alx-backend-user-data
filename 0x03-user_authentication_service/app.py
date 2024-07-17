#!/usr/bin/env python3
""" basic flask app """
from flask import Flask, jsonify, request
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



if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
