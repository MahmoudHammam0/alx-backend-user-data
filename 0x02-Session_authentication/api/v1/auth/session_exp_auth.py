#!/usr/bin/env python3
""" Expiration class for session authentication module """
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from os import environ


class SessionExpAuth(SessionAuth):
    """ Expiration class for session auth """
    def __init__(self):
        """ initialization """
        try:
            self.session_duration = int(environ.get('SESSION_DURATION'))
        except ValueError:
            self.session_duration = 0

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

        session_dict = self.user_id_by_session_id[session_id]
        if not session_dict:
            return None

        if self.session_duration <= 0:
            return user_id

        created_at = session_dict['created_at']
        if not created_at:
            return None

        now = datetime.now()

        check_time = created_at + timedelta(seconds=self.session_duration)
        if check_time < now:
            return None

        return session_dict['user_id']
