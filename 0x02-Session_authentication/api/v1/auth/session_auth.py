#!/usr/bin/env python3
""" session authentication module """
from api.v1.auth.auth import Auth
import uuid
from models.user import User
from typing import TypeVar


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

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ return User for the specific session id """
        if not session_id or type(session_id) != str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> TypeVar('User'):
        """ return a User based on the cookie value """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        user = User.get(user_id)
        return user

    def destroy_session(self, request=None) -> bool:
        """ deletes the user session / logout """
        if not request:
            return False
        if not self.session_cookie(request):
            return False
        session_id = self.session_cookie(request)
        if not self.user_id_for_session_id(session_id):
            return False
        del self.user_id_by_session_id[session_id]
        return True
