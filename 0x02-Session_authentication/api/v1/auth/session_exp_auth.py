#!/usr/bin/env python3
""" Expiration class for session authentication module """
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from os import getenv


class SessionExpAuth(SessionAuth):
    """ Expiration class for session auth """
    def __init__(self):
        """ initialization """
        super().__init__()
        try:
            exp = int(getenv('SESSION_DURATION', 0))
        except ValueError:
            exp = 0

        self.session_duration = exp

    def create_session(self, user_id=None) -> str:
        """ create session overload """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        session_dictionary = {"user_id": user_id, "created_at": datetime.now()}
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None) -> str:
        """ return user_id based on the session_id """
        if not session_id:
            return None

        session_dict = self.user_id_by_session_id.get(session_id)
        if not session_dict:
            return None

        if not session_dict.get('user_id'):
            return None

        if self.session_duration <= 0:
            return session_dict.get('user_id')

        created_at = session_dict.get('created_at')
        if not created_at:
            return None

        check_time = created_at + timedelta(seconds=self.session_duration)
        if check_time < datetime.now():
            return None

        return session_dict.get('user_id')
