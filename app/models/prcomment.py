from flask import current_app as app
import sys

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
ORDER BY votes DESC, time_commented DESC
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


    @staticmethod
    def upvote_comment(pid, uid, rid):
        app.db.execute('''
    UPDATE PR_Comments
    SET votes = votes + 1
    WHERE PR_Comments.pid = :pid AND PR_Comments.uid = :uid AND PR_Comments.rid = :rid
    RETURNING *;
    ''',  
                               uid = uid, pid = pid, rid = rid)

    @staticmethod
    def downvote_comment(pid, uid, rid):
        app.db.execute('''
    UPDATE PR_Comments
    SET votes = votes - 1
    WHERE PR_Comments.pid = :pid AND PR_Comments.uid = :uid AND PR_Comments.rid = :rid
    RETURNING *;
    ''',  
                               uid = uid, pid = pid, rid = rid)


    @staticmethod
    def addcomment(rid, uid, pid, time_reviewed, comments, votes):
        try:
        #     print('this is the email: ' + email, file=sys.stderr)
        #     print('this is the password: ' + password, file=sys.stderr)
        #     print('this is the firstname: ' + firstname, file=sys.stderr)
            print('this is the comment: ' + comments, file=sys.stderr)

            rows = app.db.execute("""
INSERT INTO PR_Comments
VALUES(:rid, :uid, :pid, :time_reviewed, :comments, :votes)
RETURNING pid
""",
                                  rid = rid,
                                  uid = uid,
                                  pid = pid,
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