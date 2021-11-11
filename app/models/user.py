from __future__ import print_function # In python 2.7
import sys
from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash

from .. import login


class User(UserMixin):
    def __init__(self, uid, email, firstname, lastname):
        self.uid = uid
        self.email = email
        self.firstname = firstname
        self.lastname = lastname


    @staticmethod
    def get_by_auth(email, password):
        rows = app.db.execute("""
SELECT password, uid, email, firstname, lastname
FROM Users
WHERE email = :email
""",
                              email=email)
        if not rows:  # email not found
            return None
        elif not check_password_hash(rows[0][0], password):
            # incorrect password
            return None
        else:
            return User(*(rows[0][1:]))

    @staticmethod
    def email_exists(email):
        rows = app.db.execute("""
SELECT email
FROM Users
WHERE email = :email
""",
                              email=email)
        return len(rows) > 0

    @staticmethod
    def register(email, password, firstname, lastname):
        try:
            print('this is the email: ' + email, file=sys.stderr)
            print('this is the password: ' + password, file=sys.stderr)
            print('this is the firstname: ' + firstname, file=sys.stderr)
            print('this is the lastname: ' + lastname, file=sys.stderr)
            rows = app.db.execute("""
INSERT INTO Users(email, firstname, lastname, password)
VALUES(:email, :firstname, :lastname, :password)
RETURNING uid
""",
                                  email=email,
                                  firstname=firstname,
                                  lastname=lastname,
                                  password=generate_password_hash(password))
            # print('go wrong 1', file=sys.stderr)
            uid = rows[0][0]
            # print('go wrong 2', file=sys.stderr)
            return User.get(uid)
        except Exception:
            print('made it to the exception', file=sys.stderr)
            # likely email already in use; better error checking and
            # reporting needed
            return None

    @staticmethod
    @login.user_loader
    def get(uid):
        rows = app.db.execute("""
SELECT uid, email, firstname, lastname
FROM Users
WHERE uid = :uid
""",
                              uid=uid)
        return User(*(rows[0])) if rows else None
