from flask import current_app as app
from flask_login import current_user
import sys

#Orders(oid, uid, total_price, fulfilled, time_purchased)
#OrderedItems(oid, pid, total_price, p_quantity, fulfilled, fulfillment_time)

class pastOrders:
    def __init__(self, oid, uid, total_price, fulfilled, time_purchased):
        self.oid = oid 
        self.uid = uid
        self.total_price = total_price
        self.fulfilled = fulfilled
        self.time_purchased = time_purchased 
        

    @staticmethod
    def get_orders(uid):
        rows = app.db.execute('''
    SELECT *
    FROM Orders
    WHERE uid = :uid
    ''',  
                               uid = uid)
        return [pastOrders(*row) for row in rows] if rows is not None else None
    