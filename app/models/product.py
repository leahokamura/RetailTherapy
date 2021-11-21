from flask import current_app as app


class Product:
    def __init__(self, pid, name, price, available, description, category):
        self.pid = pid
        self.name = name
        self.price = price
        self.available = available
        self.description = description
        self.category = category

    @staticmethod
    def get(pid):
        rows = app.db.execute('''
SELECT pid, name, price, available, description, category
FROM Products
WHERE pid = :pid
''',
                              pid=pid)
        return Product(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all(available=True):
        rows = app.db.execute('''
SELECT pid, name, price, available, description, category
FROM Products
WHERE available = :available
''',
                              available=available)
        return [Product(*row) for row in rows]

    @staticmethod
    def get_name(pid):
        rows = app.db.execute('''
SELECT pid, name
FROM Products
WHERE pid = :pid
''',
                            pid=pid)
        return (rows[0]) if rows else None

    @staticmethod
    def get_prod_by_cat(category):
        rows = app.db.execute('''
SELECT pid, name, price, available, description, category
FROM Products
WHERE category = :category
''',        
                            category=category)
        return [Product(*row) for row in rows] if rows else None

    @staticmethod
    def get_categories():
        rows = app.db.execute('''
SELECT DISTINCT category FROM products      
''')
        return [(row[0]) for row in rows] if rows else None