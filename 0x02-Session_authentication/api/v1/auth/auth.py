#!/usr/bin/env python3
""" Authentication class module """
from flask import request
from typing import List, TypeVar
import fnmatch
from os import environ


class Auth:
    """ authentication class """
    def __init__(self):
        """ initialization """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ checks if the path in excluded paths """
        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        for pattern in excluded_paths:
            if fnmatch.fnmatch(path, pattern):
                return False
            if fnmatch.fnmatch(path + "/", pattern):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """ validate requests headers for Authorization """
        if request is None or "Authorization" not in request.headers.keys():
            return None
        return request.headers["Authorization"]

    def current_user(self, request=None) -> TypeVar('User'):
        """ Not Implemented yet """
        return None

    def session_cookie(self, request=None):
        """ returns a cookie value from a request """
        if not request:
            return None
        cookie_name = environ.get('SESSION_NAME')
        return request.cookies.get(cookie_name)
