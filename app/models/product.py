from __future__ import print_function # In python 2.7
from flask import current_app as app
from sqlalchemy import text

import sys

import sqlalchemy

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

#     @staticmethod
#     def get_prod_by_cat(category, sortCriteria):
        rows = app.db.execute('''
WITH prod_rating  AS (
SELECT pid, AVG(rating)::numeric(10,2) AS avg
FROM Product_Reviews
GROUP BY pid)
SELECT Products.pid, Products.name, Products.price, prod_rating.avg AS rating
FROM Products
FULL OUTER JOIN
prod_rating
ON prod_rating.pid = Products.pid
WHERE Products.category = :category
''', category=category)
        return rows if rows else None
    
    
    
    # this is the one that works 
    @staticmethod
    def get_prod_by_cat(category, sortCriteria):
        
        sorting_descrip = ''

        if (sortCriteria == 'high'):
            sorting_descrip = '''price DESC'''
        if (sortCriteria == 'low'):
            sorting_descrip = '''price ASC'''
        if (sortCriteria == 'high_rating'):
            sorting_descrip = '''rating DESC NULLS LAST'''
        if (sortCriteria == 'low_rating'):
            sorting_descrip = '''rating ASC NULLS LAST'''

        rows = app.db.execute('''
WITH prod_rating  AS (
SELECT pid, AVG(rating)::numeric(10,2) AS avg
FROM Product_Reviews
GROUP BY pid)
SELECT Products.pid, Products.name, Products.price, prod_rating.avg AS rating
FROM Products
FULL OUTER JOIN
prod_rating
ON prod_rating.pid = Products.pid
WHERE Products.category = :category
ORDER BY ''' + sorting_descrip, 
category=category)
        
        return rows if rows else None

#         rows = app.db.execute('''
# SELECT pid, name, price, available, description, category
# FROM Products
# WHERE category = :category
# ORDER BY ''' + sorting_descrip,
# category=category)
# return [Product(*row) for row in rows] if rows else None

    @staticmethod
    def get_categories():
        rows = app.db.execute('''
SELECT DISTINCT category FROM products      
''')
        return [(row[0]) for row in rows] if rows else None

    # can only search for one keyword at a time
#     @staticmethod
#     def get_by_keyword(word):
#         rows = app.db.execute('''
# SELECT pid, name, price, available, description, category 
# FROM Products 
# WHERE name LIKE :word
# OR description LIKE :word
# ''',
#                             word = '%' + word + '%')
#         return [Product(*row) for row in rows] if rows else None

    # this is the one that works
    # @staticmethod
#     def get_by_keyword(words, sortCriteria):
#         if (sortCriteria == 'high'):
#             rows = app.db.execute('''
# SELECT pid, name, price, available, description, category
# FROM Products
# WHERE name LIKE ANY (:words)
# OR description LIKE ANY (:words)
# ORDER BY price DESC      
# ''', words = words)

#         if (sortCriteria == 'low'):
#             rows = app.db.execute('''
# SELECT pid, name, price, available, description, category
# FROM Products
# WHERE name LIKE ANY (:words)
# OR description LIKE ANY (:words)
# ORDER BY price ASC      
# ''', words = words)
#         return [Product(*row) for row in rows] if rows else None
    @staticmethod
    def get_by_keyword(words, sortCriteria):
        
        sorting_descrip = ''

        if (sortCriteria == 'high'):
            sorting_descrip = '''price DESC'''
        if (sortCriteria == 'low'):
            sorting_descrip = '''price ASC'''
        if (sortCriteria == 'high_rating'):
            sorting_descrip = '''rating DESC NULLS LAST'''
        if (sortCriteria == 'low_rating'):
            sorting_descrip = '''rating ASC NULLS LAST'''
        
        rows = app.db.execute('''
SELECT pid, name, price, available, description, category
FROM Products
WHERE name LIKE ANY (:words)
OR description LIKE ANY (:words)
ORDER BY ''' + sorting_descrip,    
words = words)

        return rows if rows else None
