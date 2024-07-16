#!/usr/bin/env python3
""" Auth module """
import bcrypt
from db import DB
from user import User


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
        session = self._db._session
        user = session.query(User).filter_by(email=email).first()
        if user:
            raise ValueError(f'User {email} already exists')
        hashed_pw = _hash_password(password)
        new_user = User(email=email, hashed_password=hashed_pw)
        session.add(new_user)
        session.commit()
        return new_user
