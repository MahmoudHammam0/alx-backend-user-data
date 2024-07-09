#!/usr/bin/env python3
""" Authentication class module """
from flask import request
from typing import List, TypeVar


class Auth:
    """ authentication class """
    def __init__(self):
        """ initialization """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ checks if the path in excluded paths """
        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        slash_path = path + "/"
        if path in excluded_paths or slash_path in excluded_paths:
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
