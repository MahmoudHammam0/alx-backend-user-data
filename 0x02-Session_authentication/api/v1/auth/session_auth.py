#!/usr/bin/env python3
""" session authentication module """
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """ session authentication class """
    def __init__(self):
        """ initialization """
