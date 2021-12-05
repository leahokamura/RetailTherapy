from flask import current_app as app

import sys

class SellerReview:
    def __init__(self, uid, seller_id, time_reviewed, rating, comments, votes):
        self.uid = uid
        self.seller_id = seller_id
        self.time_reviewed = time_reviewed
        self.rating = rating
        self.comments = comments
        self.votes = votes
        
    @staticmethod
    def get_all_seller_reviews_for_seller(seller_id):
        rows = app.db.execute('''
SELECT uid, seller_id, time_reviewed, rating, comments, votes
FROM Seller_Reviews
WHERE seller_id = :seller_id
ORDER BY votes DESC, time_reviewed DESC
''',
                              seller_id=seller_id)
        return [SellerReview(*row) for row in rows]
        
    @staticmethod
    def get_seller_avg_rating(pid):
        rows = app.db.execute('''
SELECT MAX(uid), MAX(seller_id), MAX(time_reviewed), AVG(rating)::numeric(10,2) AS avg, MAX(comments), MAX(votes)
FROM Seller_Reviews
WHERE seller_id = :seller_id
''',
                              seller_id=seller_id)
        return SellerReview(*(rows[0])) if rows else None

    @staticmethod
    def get_stats(seller_id):
        rows = app.db.execute('''
SELECT COUNT(uid) AS number, MAX(seller_id) AS seller_id, MAX(time_reviewed), AVG(rating)::numeric(10,2) AS average, MAX(comments), MAX(votes)
FROM Seller_Reviews
WHERE seller_id = :seller_id
''',
                              seller_id=seller_id)
        print(rows[0][3])
        return (rows[0]) if rows else None

    @staticmethod
    def get_all_seller_reviews_by_user(uid):
        rows = app.db.execute('''
SELECT seller_id, uid, time_reviewed, rating, comments, votes
FROM Seller_Reviews
WHERE uid = :uid
''',
                              uid=uid)
        return [SellerReview(*row) for row in rows]

    @staticmethod
    def get_all_seller_reviews_for_seller_and_user(seller_id, uid):
        rows = app.db.execute('''
SELECT uid, seller_id, time_reviewed, rating, comments, votes
FROM Seller_Reviews
WHERE seller_id = :seller_id AND uid = :uid
ORDER BY votes DESC
''',
                              seller_id=seller_id, uid=uid)
        return (rows[0]) if rows else None


    @staticmethod
    def upvote_review(seller_id, uid):
        app.db.execute('''
    UPDATE Seller_Reviews
    SET votes = votes + 1
    WHERE Seller_Reviews.seller_id = :seller_id AND Product_Reviews.uid = :uid
    RETURNING *
    ''',  
                               uid = uid, seller_id = seller_id)



    @staticmethod
    def addreview(uid, seller_id, time_reviewed, rating, comments, votes):
        try:
        #     print('this is the email: ' + email, file=sys.stderr)
        #     print('this is the password: ' + password, file=sys.stderr)
        #     print('this is the firstname: ' + firstname, file=sys.stderr)
            print('this is the comment: ' + comments, file=sys.stderr)
            print('this is the rating: ' + str(rating), file=sys.stderr)

            rows = app.db.execute("""
INSERT INTO Seller_Reviews
VALUES(:uid, :seller_id, :time_reviewed, :rating, :comments, :votes)
RETURNING seller_id
""",
                                  uid = uid,
                                  seller_id = seller_id,
                                  time_reviewed = time_reviewed,
                                  rating = rating,
                                  comments = comments,
                                  votes = votes)

            print('this worked!', file = sys.stderr)
            return True
        except Exception:
            print('bad things happening', file = sys.stderr)
            return None


    def get_just_rating(seller_id):
        rows = app.db.execute('''
SELECT MAX(pid) as seller_id, AVG(rating)::numeric(10,2) AS avg
FROM Seller_Reviews
WHERE seller_id = :seller_id       
''',  
        seller_id = seller_id)
        return (rows[0]) if rows else None

    @staticmethod
    def editreview(uid, seller_id, time_reviewed, rating, comments, votes):
        try:
        #     print('this is the email: ' + email, file=sys.stderr)
        #     print('this is the password: ' + password, file=sys.stderr)
        #     print('this is the firstname: ' + firstname, file=sys.stderr)
            print('this is the comment: ' + comments, file=sys.stderr)
            print('this is the rating: ' + str(rating), file=sys.stderr)

            rows = app.db.execute("""
UPDATE Seller_Reviews
SET rating = :rating, comments = :comments
WHERE Seller_Reviews.uid = :uid AND Seller_Reviews.seller_id = :seller_id
RETURNING seller_id
""",
                                  uid = uid,
                                  seller_id = seller_id,
                                  time_reviewed = time_reviewed,
                                  rating = rating,
                                  comments = comments,
                                  votes = votes)

            print('this worked!', file = sys.stderr)
            return True
        except Exception:
            print('bad things happening', file = sys.stderr)
            return None
