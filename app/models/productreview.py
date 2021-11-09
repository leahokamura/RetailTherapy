from flask import current_app as app

class ProductReview:
    def __init__(self, uid, pid, time_reviewed, rating, comments, votes):
        self.uid = uid
        self.pid = pid
        self.time_reviewed = time_reviewed
        self.rating = rating
        self.comments = comments
        self.votes = votes

    @staticmethod
    def get_all_product_reviews_for_product(pid):
        rows = app.db.execute('''
SELECT uid, pid, time_reviewed, rating, comments, votes
FROM Product_Reviews
WHERE pid = :pid
''',
                              pid=pid)
        return [ProductReview(*row) for row in rows]

    @staticmethod
    def get_all_product_reviews_by_user(uid):
        rows = app.db.execute('''
SELECT pid, uid, time_reviewed, rating, comments, votes
FROM Product_Reviews
WHERE uid = :uid
''',
                              uid=uid)
        return [ProductReview(*row) for row in rows]
