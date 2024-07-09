#!/usr/bin/env python3
""" basic authentication class module """
from flask import request
from typing import List, TypeVar
from api.v1.auth.auth import Auth
import base64
from models.user import User


class BasicAuth(Auth):
    """ Basic authentication class """
    def __init__(self):
        """ initialization """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ returns the Base64 part of the Authorization header """
        if not authorization_header or type(authorization_header) != str:
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split()[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """ returns the decoded value of a Base64 string """
        if not base64_authorization_header or\
                type(base64_authorization_header) != str:
            return None
        try:
            data = base64.b64decode(base64_authorization_header)
        except Exception:
            return None
        return data.decode('utf-8')

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """ returns the user email and password from decoded value """
        if not decoded_base64_authorization_header or\
                type(decoded_base64_authorization_header) != str:
            return (None, None)
        if ":" not in decoded_base64_authorization_header:
            return (None, None)
        credentials = decoded_base64_authorization_header.split(":")
        return (credentials[0], credentials[1])

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """ returns the User instance based on his email and password """
        if not user_email or type(user_email) != str:
            return None
        if not user_pwd or type(user_pwd) != str:
            return None
        try:
            users_list = User.search({"email": user_email})
        except Exception:
            return None
        for user in users_list:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ overloads Auth and retrieves the User instance for a request """
        auth_header = self.authorization_header(request)
        bs64_cred = self.extract_base64_authorization_header(auth_header)
        credentials = self.decode_base64_authorization_header(bs64_cred)
        user_email, password = self.extract_user_credentials(credentials)
        user = self.user_object_from_credentials(user_email, password)
        return user
