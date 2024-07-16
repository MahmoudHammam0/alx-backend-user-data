#!/usr/bin/env python3
""" Auth module """
import bcrypt


def _hash_password(password: str) -> bytes:
    """ used to hash the password using bcrypt """
    encoded_password = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_pass = bcrypt.hashpw(encoded_password, salt)
    return hashed_pass
