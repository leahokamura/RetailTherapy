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
ORDER BY votes DESC, time_reviewed DESC
''',
                              pid=pid)
        return [ProductReview(*row) for row in rows]
        
    @staticmethod
    def get_product_avg_rating(pid):
        rows = app.db.execute('''
SELECT MAX(uid), MAX(pid), MAX(time_reviewed), AVG(rating)::numeric(10,2) AS avg, MAX(comments), MAX(votes)
FROM Product_Reviews
WHERE pid = :pid
''',
                              pid=pid)
        return ProductReview(*(rows[0])) if rows else None

    @staticmethod
    def get_stats(pid):
        rows = app.db.execute('''
SELECT COUNT(uid) AS number, MAX(pid) AS pid, MAX(time_reviewed), AVG(rating)::numeric(10,2) AS average, MAX(comments), MAX(votes)
FROM Product_Reviews
WHERE pid = :pid
''',
                              pid=pid)
        print(rows[0][3])
        return (rows[0]) if rows else None

    @staticmethod
    def get_all_product_reviews_by_user(uid):
        rows = app.db.execute('''
SELECT pid, uid, time_reviewed, rating, comments, votes
FROM Product_Reviews
WHERE uid = :uid
''',
                              uid=uid)
        return [ProductReview(*row) for row in rows]

    @staticmethod
    def get_all_product_reviews_for_product_and_user(pid, uid):
        rows = app.db.execute('''
SELECT uid, pid, time_reviewed, rating, comments, votes
FROM Product_Reviews
WHERE pid = :pid AND uid = :uid
ORDER BY votes DESC
''',
                              pid=pid, uid=uid)
        return (rows[0]) if rows else None


    @staticmethod
    def upvote_review(pid, uid):
        app.db.execute('''
    UPDATE Product_Reviews
    SET votes = votes + 1
    WHERE Product_Reviews.pid = :pid AND Product_Reviews.uid = :uid
    RETURNING *;
    ''',  
                               uid = uid, pid = pid)