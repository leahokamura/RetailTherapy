from flask import current_app as app
from flask_login import current_user
import sys

#Orders(oid, uid, total_price, fulfilled, time_purchased)
#OrderedItems(oid, pid, unit_price, p_quantity, fulfilled, fulfillment_time)

class pastOrders:
    def __init__(self, oid, uid, total_price, fulfilled, time_purchased, unit_price= None):
        self.oid = oid 
        self.uid = uid
        self.total_price = total_price
        self.fulfilled = fulfilled
        self.time_purchased = time_purchased
        self.unit_price = unit_price

        

    @staticmethod
    def get_orders(uid):
        rows = app.db.execute('''
    SELECT *
    FROM Orders
    WHERE uid = :uid
    ORDER BY time_purchased
    DESC
    ''',  
                               uid = uid)
        return [pastOrders(*row) for row in rows] if rows is not None else None


    @staticmethod
    def get_orderedProducts(uid, oid):
        rows = app.db.execute('''
    SELECT OrderedItems.pid AS pid, name AS name, p_quantity AS p_quantity, unit_price AS unit_price, fulfilled AS fulfilled, fulfillment_time AS fulfillment_time
    FROM OrderedItems, Products
    WHERE uid = :uid AND oid = :oid AND OrderedItems.pid = Products.pid
    ORDER BY pid
    DESC
    ''',  
                               uid = uid, oid=oid)
        return [row for row in rows] if rows is not None else None

    @staticmethod
    def get_status(uid):
        