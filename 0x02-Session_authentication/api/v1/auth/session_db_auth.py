#!/usr/bin/env python3
"""
SessionDBAuth class module
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """ SessionDBAuth class """

    def create_session(self, user_id=None):
        """ Creates a session for the user """
        session_id = super().create_session(user_id)
        if not session_id or not isinstance(session_id, str):
            return None

        kwargs = {
            'user_id': user_id,
            'session_id': session_id,
        }
        user_session = UserSession(**kwargs)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Returns a User ID based on a Session ID """
        try:
            user_session = UserSession.search({'session_id': session_id})
        except Exception:
            return None

        if not user_session:
            return None

        created_at = user_session[0].created_at
        duration = timedelta(seconds=self.session_duration)
        if (created_at + duration) < datetime.now():
            return None

        return user_session[0].user_id

    def destroy_session(self, request=None):
        """ Deletes the user session / logout """
        session_id = self.session_cookie(request)

        try:
            user_session = UserSession.search({'session_id': session_id})
        except Exception:
            return False

        if not user_session:
            return False

        user_session[0].remove()

        return True
