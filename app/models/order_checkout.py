from flask import current_app as app
from flask_login import current_user
import sys

#Orders(oid, uid, total_price, fulfilled, time_purchased)
#OrderedItems(oid, pid, total_price, p_quantity, fulfilled, fulfillment_time)

class Order:
    def __init__(oid, uid, total_price, fulfilled, time_purchased, pid, fulfillment_time):
        self.uid = uid
        self.pid = pid
        self.name = name
        self.p_quantity = p_quantity
        self.total_price = total_price
        self.fulfilled = fulfilled
        self.time_purchased = time_purchased 
        self.oid = self.pid 
        self.fulfillment_time = fulfillment_time

    def addToOrders(uid, total_price, time_purchased):
        rows = app.db.execute('''
    SELECT COUNT(uid) FROM Orders
    ''')
        oid = rows[0][0]
        if oid == None:
            oid = 0
        oid = int(oid + 1)

        rows = app.db.execute('''
    INSERT INTO Orders(oid, uid, total_price, fulfilled, time_purchased)
    VALUES (:oid, :uid, :total_price, FALSE, :time_purchased)
    RETURNING *;
    ''',  
                               uid = uid, total_price = total_price, time_purchased = time_purchased, oid = oid)
        print(rows)
    
    @staticmethod
    def get_balance(uid):
        rows = app.db.execute('''
    SELECT balance FROM Account WHERE uid = :uid''', 
                uid = uid
            )
        user_balance = float(rows[0][0])
        return user_balance
