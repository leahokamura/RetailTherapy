from flask import current_app as app


class Cart:
    def __init__(self, cid, p_quantity, unit_price, total_price, pid, uid):
        self.cid = cid
        self.p_quantity = p_quantity

    @staticmethod
    def get_cart(uid):
        rows = app.db.execute('''
SELECT cid, p_quantity, unit_price, total_price, pid, uid
FROM InCart
WHERE uid = :uid
''',
                              uid=uid)
        return [Cart(*row) for row in rows] if rows is not None else None

#     @staticmethod
#     def get(pid):
#         rows = app.db.execute('''
# SELECT pid, name, price, available
# FROM Products
# WHERE pid = :pid
# ''',
#                               pid=pid)
#         return Product(*(rows[0])) if rows is not None else None

#     @staticmethod
#     def get_all(available=True):
#         rows = app.db.execute('''
# SELECT pid, name, price, available
# FROM Products
# WHERE available = :available
# ''',
#                               available=available)
#         return [Product(*row) for row in rows]
