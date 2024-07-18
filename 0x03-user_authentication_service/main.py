#!/usr/bin/env python3
""" integration test module """
import requests


def register_user(email: str, password: str) -> None:
    """ register user test """
    r = requests.post("http://localhost:5000/users",
                      data={"email": email, "password": password})
    assert r.status_code == 200
    assert r.json() == {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """ test login with wrong password """
    r = requests.post('http://localhost:5000/sessions',
                      data={"email": email, "password": password})
    assert r.status_code == 401


def log_in(email: str, password: str) -> str:
    """ test login with correct credentials """
    r = requests.post('http://localhost:5000/sessions',
                      data={"email": email, "password": password})
    assert r.status_code == 200
    assert r.json() == {"email": email, "message": "logged in"}
    return r.cookies.get('session_id')


def profile_unlogged() -> None:
    """ test profile route """
    r = requests.get('http://localhost:5000/profile', data={})
    assert r.status_code == 403


def profile_logged(session_id: str) -> None:
    """ test profile route with correct session_id """
    r = requests.get('http://localhost:5000/profile',
                     cookies={"session_id": session_id})
    email = r.json().get("email")
    assert r.status_code == 200
    assert r.json() == {"email": email}


def log_out(session_id: str) -> None:
    """ logout test """
    r = requests.delete('http://localhost:5000/sessions',
                        cookies={"session_id": session_id})
    assert r.status_code == 200


def reset_password_token(email: str) -> str:
    """ test reset token route """
    r = requests.post('http://localhost:5000/reset_password',
                      data={"email": email})
    assert r.status_code == 200
    reset_token = r.json().get('reset_token')
    assert r.json() == {"email": email, "reset_token": reset_token}
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ test update password """
    data = {"email": email, "reset_token": reset_token,
            "new_password": new_password}
    r = requests.put('http://localhost:5000/reset_password', data=data)
    assert r.status_code == 200
    assert r.json() == {"email": email, "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
