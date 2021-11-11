from flask import current_app as app


class Profile:
    def __init__(self, uid, email, firstname, lastname, password, address):
        self.uid = uid
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.password = password
        self.address = address


    @staticmethod
    def get_profile(email):
        rows = app.db.execute("""
SELECT uid, email, firstname, lastname, password, address
FROM Users
WHERE email = :email AND password = :password
""",
        email=email)
        return [Profile(*(rows[0])) if rows is not None else None]

    
    @staticmethod
    def get_public(uid):
        rows = app.db.execute("""
SELECT uid, firstname
FROM Users
WHERE uid = :uid
""",
        uid=uid)
        return [Profile(*(rows[0])) if rows is not None else None]
