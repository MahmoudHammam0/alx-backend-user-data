#!/usr/bin/env python3
""" Auth module """
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """ used to hash the password using bcrypt """
    encoded_password = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_pass = bcrypt.hashpw(encoded_password, salt)
    return hashed_pass


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self) -> None:
        """ initialization """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ register a new user and return a User object """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_pw = _hash_password(password)
            new_user = self._db.add_user(email, hashed_pw)
            return new_user
        else:
            raise ValueError(f'User {email} already exists')

    def valid_login(self, email: str, password: str) -> bool:
        """ validate the login credentials """
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            return False
        res = bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)
        if not res:
            return False
        return True
