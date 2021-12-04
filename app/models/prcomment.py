from flask import current_app as app

class PR_Comment:
    def __init__(self, rid, uid, pid, time_commented, comment, votes):
        self.rid = rid
        self.uid = uid
        self.pid = pid
        self.time_commented = time_commented
        self.comment = comment
        self.votes = votes

    @staticmethod
    def get_all_product_review_comments(pid, uid):
        rows = app.db.execute('''
SELECT rid, uid, pid, time_commented, comment, votes
FROM PR_Comments
WHERE pid = :pid AND uid = :uid
''',
                              pid=pid, uid=uid)
        return [PR_Comment(*row) for row in rows]

    @staticmethod
    def upvote_review(pid, uid):
        app.db.execute('''
    UPDATE Product_Reviews
    SET votes = votes + 1
    WHERE Product_Reviews.pid = :pid AND Product_Reviews.uid = :uid
    RETURNING *;
    ''',  
                               uid = uid, pid = pid)

    @staticmethod
    def downvote_review(pid, uid):
        app.db.execute('''
    UPDATE Product_Reviews
    SET votes = votes - 1
    WHERE Product_Reviews.pid = :pid AND Product_Reviews.uid = :uid
    RETURNING *;
    ''',  
                               uid = uid, pid = pid)