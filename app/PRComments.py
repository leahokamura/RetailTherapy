from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
import datetime

from .models.productreview import ProductReview
from .models.prcomment import PR_Comment
from .models.product import Product

from flask import current_app as app

from flask import Blueprint
# import sys
bp = Blueprint('pr_comments', __name__)

@bp.route('/pr_comments/product<int:product_number>/user<int:user_id>', methods=['GET', 'POST'])
def ProductReviews(product_number, user_id):
    # get all reviews for a certain product:
    p_reviews = ProductReview.get_all_product_reviews_for_product_and_user(product_number, user_id)
    # print(p_reviews, file=sys.stderr)
    review_comments = PR_Comment.get_all_product_review_comments(product_number, user_id)
    #p_r_avg = ProductReview.get_product_avg_rating(1)
    #product_review_stats = ProductReview.get_stats(product_number)

    product_name = Product.get_name(product_number)
    
    # render the page by adding information to the ProductReviews.html file
    return render_template('PRComments.html',
                            productreviews = p_reviews,
                            productreviewcomments = review_comments,
                            productname = product_name)


@bp.route('/pr_comments/product<int:product_number>/user<int:user_id>/upvote', methods=['GET', 'POST'])
def upvote(product_number, user_id):
    PR_Comment.upvote_review(product_number, user_id)
    return redirect(url_for('pr_comments.ProductReviews', product_number = product_number, user_id = user_id))

@bp.route('/pr_comments/product<int:product_number>/user<int:user_id>/downvote', methods=['GET', 'POST'])
def downvote(product_number, user_id):
    PR_Comment.downvote_review(product_number, user_id)
    return redirect(url_for('pr_comments.ProductReviews', product_number = product_number, user_id = user_id))
