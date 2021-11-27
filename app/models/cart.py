from flask import current_app as app


class Cart:
    def __init__(self, uid, pid, name, p_quantity, unit_price, seller_id):
        self.uid = uid
        self.pid = pid
        self.name = name
        self.p_quantity = p_quantity
        self.unit_price = unit_price
        self.seller_id = seller_id
    

    @staticmethod
    def get_cart(uid):
        rows = app.db.execute('''
SELECT uid, pid, name, p_quantity, unit_price, seller_id
FROM InCart
WHERE uid = :uid
''',
                              uid=uid)
        print("got cart data")
        print([Cart(*row) for row in rows])
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



#rehuhsdihfgisdhiug
