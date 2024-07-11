#!/usr/bin/env python3
""" session authentication module """
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """ session authentication class """

    user_id_by_session_id = {}

    def __init__(self):
        """ initialization """

    def create_session(self, user_id: str = None) -> str:
        """ creates a session for the user with the specific id """
        if not user_id or type(user_id) != str:
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id
