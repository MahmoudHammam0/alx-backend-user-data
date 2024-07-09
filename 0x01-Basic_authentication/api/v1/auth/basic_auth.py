#!/usr/bin/env python3
""" basic authentication class module """
from flask import request
from typing import List, TypeVar
from api.v1.auth.auth import Auth
import base64


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
