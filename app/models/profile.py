from __future__ import print_function # In python 2.7
import sys
from flask_login import UserMixin
from flask import current_app as app

from .. import login


class User(UserMixin):
    def __init__(self, uid, email, firstname, lastname):
        self.uid = uid
        self.email = email
        self.firstname = firstname
        self.lastname = lastname

    @staticmethod
    def get_profile(uid):
        rows = app.db.execute("""
SELECT uid, email, firstname, lastname, password, address
FROM Users
WHERE uid = :uid
""",
                            uid=uid)
        return User(*(rows[0])) if rows else None


    @staticmethod
    def get_public(uid):
        rows = app.db.execute("""
SELECT uid, firstname
FROM Users
WHERE uid = :uid
""",
                            uid=uid)
        return User(*(rows[0])) if rows else None