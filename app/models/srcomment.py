from flask import current_app as app
import sys

class SR_Comment:
    def __init__(self, rid, uid, seller_id, time_commented, comment, votes):
        self.rid = rid
        self.uid = uid
        self.seller_id = seller_id
        self.time_commented = time_commented
        self.comment = comment
        self.votes = votes

    @staticmethod
    def get_all_seller_review_comments(seller_id, uid):
        rows = app.db.execute('''
SELECT rid, uid, seller_id, time_commented, comment, votes
FROM SR_Comments
WHERE seller_id = :seller_id AND uid = :uid
ORDER BY votes DESC, time_commented DESC
''',
                              seller_id=seller_id, uid=uid)
        return [SR_Comment(*row) for row in rows]

    @staticmethod
    def upvote_review(seller_id, uid):
        app.db.execute('''
    UPDATE Seller_Reviews
    SET votes = votes + 1
    WHERE Seller_Reviews.seller_id = :seller_id AND Seller_Reviews.uid = :uid
    RETURNING *;
    ''',  
                               uid = uid, seller_id = seller_id)

    @staticmethod
    def downvote_review(seller_id, uid):
        app.db.execute('''
    UPDATE Seller_Reviews
    SET votes = votes - 1
    WHERE Seller_Reviews.seller_id = :seller_id AND Seller_Reviews.uid = :uid
    RETURNING *;
    ''',  
                               uid = uid, seller_id = seller_id)


    @staticmethod
    def upvote_comment(seller_id, uid, rid):
        app.db.execute('''
    UPDATE SR_Comments
    SET votes = votes + 1
    WHERE SR_Comments.seller_id = :seller_id AND SR_Comments.uid = :uid AND SR_Comments.rid = :rid
    RETURNING *;
    ''',  
                               uid = uid, seller_id = seller_id, rid = rid)

    @staticmethod
    def downvote_comment(seller_id, uid, rid):
        app.db.execute('''
    UPDATE SR_Comments
    SET votes = votes - 1
    WHERE SR_Comments.seller_id = :seller_id AND SR_Comments.uid = :uid AND SR_Comments.rid = :rid
    RETURNING *;
    ''',  
                               uid = uid, seller_id = seller_id, rid = rid)


    @staticmethod
    def addcomment(rid, uid, seller_id, time_reviewed, comments, votes):
        try:
        #     print('this is the email: ' + email, file=sys.stderr)
        #     print('this is the password: ' + password, file=sys.stderr)
        #     print('this is the firstname: ' + firstname, file=sys.stderr)
            print('this is the comment: ' + comments, file=sys.stderr)

            rows = app.db.execute("""
INSERT INTO SR_Comments
VALUES(:rid, :uid, :seller_id, :time_reviewed, :comments, :votes)
RETURNING seller_id
""",
                                  rid = rid,
                                  uid = uid,
                                  seller_id = seller_id,
                                  time_reviewed = time_reviewed,
                                  comments = comments,
                                  votes = votes)
            #product_id = rows[0][0]
            #print('this is the pid: ' + product_id, file = sys.stderr)
            print('this worked!')
            return True
        except Exception:
            print('bad things happening', file = sys.stderr)
            return None

    @staticmethod
    def editcomment(rid, uid, seller_id, time_commented, comment, votes):
        try:
        #     print('this is the email: ' + email, file=sys.stderr)
        #     print('this is the password: ' + password, file=sys.stderr)
        #     print('this is the firstname: ' + firstname, file=sys.stderr)
            print('this is the comment: ' + comment, file=sys.stderr)

            rows = app.db.execute("""
UPDATE SR_Comments
SET comment = :comment
WHERE rid = :rid AND uid = :uid AND seller_id = :seller_id
RETURNING seller_id
""",
                                  rid = rid,
                                  uid = uid,
                                  seller_id = seller_id,
                                  time_commented = time_commented,
                                  comment = comment,
                                  votes = votes)
            #product_id = rows[0][0]
            #print('this is the pid: ' + product_id, file = sys.stderr)
            print('this worked!')
            return True
        except Exception:
            print('bad things happening', file = sys.stderr)
            return None

    @staticmethod
    def delete_comment(seller_id, uid, rid):
        app.db.execute('''
    DELETE
    FROM SR_Comments
    WHERE seller_id = :seller_id AND uid = :uid AND rid = :rid
    RETURNING *;
    ''',  
                               uid = uid, seller_id = seller_id, rid = rid)

    @staticmethod
    def delete_review(seller_id, uid):
        app.db.execute('''
    DELETE
    FROM Seller_Reviews
    WHERE seller_id = :seller_id AND uid = :uid
    RETURNING *;
    ''',  
                               uid = uid, seller_id = seller_id)