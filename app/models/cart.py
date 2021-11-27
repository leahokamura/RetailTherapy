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


#leah is also working on this ://
#     @staticmethod
#     def update(pid, uid, option):

#         rows = app.db.execute('''
# SELECT p_quantity
# FROM InCart
# WHERE uid = :uid AND pid = :pid
# ''', uid=uid, pid=pid)

#     current = int(rows[0][0])
#     updated = current + 1

# app.db.execute('''
# UPDATE Cart
# SET p_quantity = :updated
# WHERE id = :uid AND pid = :pid
# ''', uid=uid, pid=pid, updated=updated)
#         except Exception as e:
#             print(e)

# @staticmethod
#     def add(pid, uid):
#     app.db.execute(
#     '''
#         INSERT INTO InCart VALUES(:uid, :pid, :name, 1, :unit_price, :seller_id))
#     ''',                            
#                                       id = id, 
#                                       uid = uid
#             )
#         except Exception as e:
#             print(e)
 





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
