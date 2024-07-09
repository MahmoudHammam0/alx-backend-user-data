#!/usr/bin/env python3
""" basic authentication class module """
from flask import request
from typing import List, TypeVar
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """ Basic authentication class """
    def __init__(self):
        """ initialization """
