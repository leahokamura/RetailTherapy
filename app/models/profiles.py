from __future__ import print_function # In python 2.7
import sys
from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash

from .. import login

class User(UserMixin):
    def __init__(self, uid, email, firstname, lastname, password=None, address=None):
        self.uid = uid
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.password = password
        self.address = address

    @staticmethod
    def get_profile(uid):
        rows = app.db.execute("""
SELECT uid, email, firstname, lastname, password, address
FROM Users
WHERE uid = :uid
""",
                            uid=uid)
        return User(*(rows[0])) if rows else None


