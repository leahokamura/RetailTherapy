from flask import current_app as app

class ProductReviews:
    def __init__(self, pid, uid, time_reviewed, rating, comments, votes):
        self.pid = pid
	self.uid = uid
        self.time_reviewed = time_reviewed
        self.rating = rating
        self.comments = comments
	self.votes = votes

    @staticmethod
    def get_for_pid(id):
        rows = app.db.execute('''
SELECT uid, time_reviewed, rating, comments
FROM Product_Reviews
WHERE pid = :pid
''',
                              pid=pid)
        return Product_Reviews(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_for_uid(available=True):
        rows = app.db.execute('''
SELECT pid, time_reviewed, rating, comments
FROM Product_Reviews
WHERE uid = :uid
''',
                              uid=uid)
        return [Product(*row) for row in rows]
