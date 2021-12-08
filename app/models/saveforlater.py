from flask import current_app as app
from flask_login import current_user



class Later:
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
FROM SaveForLater
WHERE uid = :uid
ORDER BY pid
''',
                              uid=uid)
        print("got sfl data")
        print([row for row in rows])
        return [row for row in rows] if rows is not None else None

    @staticmethod
    def add(pid, uid):
        rows = app.db.execute('''
    INSERT INTO SaveForLater 
    SELECT :uid, :pid, name, 1, price, seller_id
    FROM Products, Inventory
    WHERE Products.pid = :pid AND Products.pid = Inventory.pid AND Inventory.in_stock > 0
    LIMIT 1
    RETURNING *;
    ''',  
                               uid = uid, pid = pid)
        print([row for row in rows])
    
    @staticmethod
    def check(pid, uid):
        rows = app.db.execute('''
    SELECT * 
    FROM SaveForLater
    WHERE uid = :uid AND pid = :pid
    ''',
                                uid = uid, 
                                pid = pid)

        if len(rows) == 0:
            return False
        else:
            return True 
    
    # @staticmethod 
    # def update(pid, uid, action):
    #     rows = app.db.execute('''
    # SELECT p_quantity
    # FROM InCart
    # WHERE uid = :uid AND pid = :pid
    # ''',
    #                             uid = uid, 
    #                             pid = pid)
    #     current_quantity = int(rows[0][0])

    #     if action == "add":
    #         quantity = current_quantity + 1
    #         app.db.execute('''
    # UPDATE InCart
    # SET p_quantity = :quantity
    # WHERE uid = :uid AND pid = :pid
    # RETURNING *
    # ''',
    #                             uid = uid, 
    #                             pid = pid,
    #                             quantity = quantity)

    #     else: 

    #         if current_quantity == 1:
    #             Cart.remove(pid,uid)
    #         else:
    #             quantity = current_quantity - 1

    #             app.db.execute('''
    # UPDATE InCart
    # SET p_quantity = :quantity
    # WHERE uid = :uid AND pid = :pid
    # RETURNING *
    # ''',
    #                             uid = uid, 
    #                             pid = pid,
    #                             quantity = quantity)

    
    @staticmethod
    def remove(pid, uid):
        app.db.execute('''
    DELETE
    FROM SaveForLater
    WHERE uid = :uid AND pid = :pid
    RETURNING *
    ''',
                                uid = uid, 
                                pid = pid)
