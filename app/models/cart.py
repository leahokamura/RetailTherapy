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
ORDER BY pid
''',
                              uid=uid)
        print("got cart data")
        print([Cart(*row) for row in rows])
        return [Cart(*row) for row in rows] if rows is not None else None

    @staticmethod
    def get_total(uid):
        rows = app.db.execute('''
SELECT SUM(InCart.p_quantity * Products.price) as total
FROM InCart, Products
WHERE InCart.pid = Products.pid AND InCart.uid = :uid
''', 
                            uid = uid)
        return rows[0][0]








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
    
    @staticmethod
    def check(pid, uid):
        rows = app.db.execute('''
    SELECT * 
    FROM InCart
    WHERE uid = :uid AND pid = :pid
    ''',
                                uid = uid, 
                                pid = pid)
    
        if len(rows) == 0:
            return False
        else:
            return True 
    
    @staticmethod 
    def update(pid, uid, action):
        rows = app.db.execute('''
    SELECT p_quantity
    FROM InCart
    WHERE uid = :uid AND pid = :pid
    ''',
                                uid = uid, 
                                pid = pid)
        current_quantity = int(rows[0][0])

        if action == "add":
            quantity = current_quantity + 1

        else: 

            if current_quantity == 1:
                Cart.remove(pid,uid)
            else:
                quantity = current_quantity - 1

                app.db.execute('''
    UPDATE InCart
    SET p_quantity = :quantity
    WHERE uid = :uid AND pid = :pid
    RETURNING *
    ''',
                                uid = uid, 
                                pid = pid,
                                quantity = quantity)

    #     rows2 = app.db.execute('''
    # SELECT p_quantity
    # FROM InCart
    # WHERE uid = :uid AND pid = :pid
    # ''',
    #                             uid = uid, 
    #                             pid = pid)
    #     current_quantity = int(rows2[0][0])
    #     if current_quantity == 0:
    #         remove(pid,uid)

    # @staticmethod
    # def check_ifZero(pid, uid):
    #     rows = app.db.execute('''
    # SELECT p_quantity
    # FROM InCart
    # WHERE uid = :uid AND pid = :pid
    # ''',
    #                             uid = uid, 
    #                             pid = pid)
    #     current_quantity = int(rows[0][0])
    #     if current_quantity > 0:
    #         return False
    #     return True

    @staticmethod
    def remove(pid, uid):
        app.db.execute('''
    DELETE
    FROM InCart
    WHERE uid = :uid AND pid = :pid
    RETURNING *
    ''',
                                uid = uid, 
                                pid = pid)
        
#         rows = app.db.execute('''
# SELECT uid, pid, name, p_quantity, unit_price, seller_id
# FROM InCart
# WHERE uid = :uid
# ORDER BY pid
# ''',
#                               uid=uid)
#         print(rows)



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
