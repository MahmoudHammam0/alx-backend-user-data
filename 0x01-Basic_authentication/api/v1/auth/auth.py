#!/usr/bin/env python3
""" Authentication class module """
from flask import request
from typing import List, TypeVar


class Auth:
    """ authentication class """
    def __init__(self):
        """ initialization """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Not Implemented yet """
        return False

    def authorization_header(self, request=None) -> str:
        """ Not Implemented yet """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Not Implemented yet """
        return None
