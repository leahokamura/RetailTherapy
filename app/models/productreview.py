from flask import current_app as app

class ProductReview:
    def __init__(self, pid, uid, time_reviewed, rating, comments, votes):
        self.pid = pid
        self.uid = uid
        self.time_reviewed = time_reviewed
        self.rating = rating
        self.comments = comments
        self.votes = votes

    @staticmethod
    def get_all_product_reviews_for_product(pid):
        rows = app.db.execute('''
SELECT uid, time_reviewed, rating, comments
FROM Product_Reviews
WHERE pid = :pid
''',
                              pid=pid)
        return [ProductReview(*row) for row in rows]

    @staticmethod
    def get_all_product_reviews_by_user(uid):
        rows = app.db.execute('''
SELECT pid, time_reviewed, rating, comments
FROM Product_Reviews
WHERE uid = :uid
''',
                              uid=uid)
        return [ProductReview(*row) for row in rows]
