from flask import current_app as app


class Seller:
    def __init__(self, uid):
        self.uid = uid

    
    @staticmethod
    def get_seller_products(uid):
        rows = app.db.execute("""
        SELECT *
        FROM Inventory
        WHERE seller_id = :uid
        """, uid=uid)

        return [Inventory(*row) for row in rows]

    @staticmethod
    def get_seller_info(uid):
        rows = app.db.execute("""
        SELECT *
        FROM Users
        WHERE uid = :uid
        """, uid=uid)

        return (rows[0]) if rows else None
