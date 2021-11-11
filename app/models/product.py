from flask import current_app as app


class Product:
    def __init__(self, pid, name, price, available):
        self.pid = id
        self.name = name
        self.price = price
        self.available = available

    @staticmethod
    def get(pid):
        rows = app.db.execute('''
SELECT id, name, price, available
FROM Products
WHERE pid = :pid
''',
                              pid=pid)
        return Product(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all(available=True):
        rows = app.db.execute('''
SELECT id, name, price, available
FROM Products
WHERE available = :available
''',
                              available=available)
        return [Product(*row) for row in rows]
