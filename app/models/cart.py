from flask import current_app as app
from flask_login import current_user


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



#--Products(pid, name, price, available, img)
#--InCart(uid, pid, name, p_quantity, unit_price, seller_id)
#--Inventory(seller_id, pid, in_stock)
    @staticmethod
    def add(pid, uid):
        app.db.execute('''
    INSERT INTO InCart 
    SELECT :uid, :pid, name, 1, price, seller_id
    FROM Products, Inventory
    WHERE Products.pid = :pid AND Products.pid = Inventory.pid AND Inventory.in_stock > 0
    LIMIT 1
    RETURNING *;
    ''',  
                               uid = uid, pid = pid)
    


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
