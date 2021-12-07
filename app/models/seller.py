from flask import current_app as app
from flask_login import current_user


class Seller:
    def __init__(self, uid):
        self.uid = uid

    
    @staticmethod
    def get_seller_products(uid):
        rows = app.db.execute("""
        SELECT  Inventory.pid AS pid,
                Products.name AS name,
                Products.price AS price,
                Products.available AS available,
                Inventory.in_stock AS in_stock
        FROM Inventory, Products
        WHERE seller_id = :uid AND Inventory.pid = Products.pid
        """, uid=uid)
        print("here:", [row for row in rows])

        return [row for row in rows]

    @staticmethod
    def get_seller_info(uid):
        rows = app.db.execute("""
        SELECT *
        FROM Users
        WHERE uid = :uid
        """, uid=uid)

        return (rows[0]) if rows else None

    @staticmethod
    def add_to_inventory(productname, price, quantity, description, image, category):
        print(productname, price, quantity, description, image, category)
        available = False
        if quantity > 0:
            available = True
        sid = current_user.uid
        new_pid = app.db.execute(
        """
        SELECT MAX(pid)
        FROM Products
        """)[0][0] + 1
        try:
            app.db.execute( # add to Products
                """
                INSERT INTO Products(pid, name, price, available, image, description, category)
                VALUES(:new_pid, :productname, :price, :available, :image, :description, :category)
                RETURNING pid
                """, new_pid=new_pid, productname=productname, price=price, available=available, description=description, image=image, category=category)
            app.db.execute( # add to Inventory
                """
                INSERT INTO Inventory(seller_id, pid, in_stock)
                VALUES(:sid, :new_pid, :quantity)
                RETURNING pid
                """, sid=sid, new_pid=new_pid, quantity=quantity
            )
            return 1
        except Exception as e:
            print("Something went wrong")
            print(str(e))

    @staticmethod
    def edit_in_inventory(pid, productname, price, quantity, description, image, category):
        print(pid, productname, price, quantity, description, image, category)
        available = False
        if quantity > 0:
            available = True
        sid = current_user.uid
        try:
            app.db.execute( # update Products
                """
                UPDATE Products
                SET name=:productname, price=:price, available=:available, description=:description, image=:image, category=:category
                WHERE pid = :pid
                RETURNING pid
                """, pid=pid, productname=productname, price=price, available=available, description=description, image=image, category=category)
            app.db.execute( # update Inventory
                """
                UPDATE Inventory
                SET in_stock=:quantity
                WHERE pid=:pid
                RETURNING pid
                """, sid=sid, pid=pid, quantity=quantity
            )
            return 1
        except Exception as e:
                print("Something went wrong")
                print(str(e))

    @staticmethod
    def delete_from_inventory(pid):
        try:
            app.db.execute(
                """
                DELETE FROM Inventory
                WHERE pid = :pid
                """, pid=pid
            )
            app.db.execute(
                """
                DELETE FROM Products
                WHERE pid = :pid
                """, pid=pid
            )
            return 1
        except Exception as e:
            print(str(e))
