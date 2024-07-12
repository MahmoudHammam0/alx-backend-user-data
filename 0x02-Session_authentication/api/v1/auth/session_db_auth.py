#!/usr/bin/env python3
""" SessionDBAuth class module """
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """ SessionDBAuth class """
    def create_session(self, user_id=None) -> str:
        """ overload of create session but with UserSession """
        session_id = super().create_session(user_id)
        if not session_id or type(session_id) != str:
            return None
        kargs = {"session_id": session_id, "user_id": user_id}
        user = UserSession(**kargs)
        user.save()
        return session_id

    def user_id_for_session_id(self, session_id=None) -> str:
        """ returns the User ID by requesting UserSession in the database """
        try:
            users_list = UserSession.search({"session_id": session_id})
        except Exception:
            return None
        if not users_list:
            return None
        created_at = users_list[0].get('created_at')
        check_time = created_at + timedelta(seconds=self.session_duration)
        if check_time < datetime.now():
            return None

        return users_list[0].get('user_id')

    def destroy_session(self, request=None) -> bool:
        """ remove the session based on the session id """
        session_id = self.session_cookie(request)
        try:
            users_list = UserSession.search({'session_id': session_id})
        except Exception:
            return False
        if not users_list:
            return False
        users_list[0].remove()
        return True
