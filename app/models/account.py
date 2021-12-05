from flask import current_app as app
from flask_login import current_user

from .. import login

class Account:
    def __init__(self, uid, balance):
        self.uid = uid
        self.balance = balance


    @staticmethod
    def update_balance(uid, balance):
        rows = app.db.execute("""
UPDATE Account
SET
    balance = CAST((balance + :balance) AS float)
WHERE uid = :uid
RETURNING *
""",
                                  uid=uid,
                                  balance=balance)
        return True


    @staticmethod
    def get_balance(uid):
        rows = app.db.execute("""
SELECT *
FROM Account
WHERE uid = :uid
""",
                              uid=uid)
        return Account(*(rows[0][1])) if rows else 0.0
