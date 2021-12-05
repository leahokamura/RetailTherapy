from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
import datetime

from .models.sellerreview import SellerReview
from .models.srcomment import SR_Comment
from .models.seller import Seller

from flask import current_app as app

from flask import Blueprint
# import sys
bp = Blueprint('sr_comments', __name__)

@bp.route('/sr_comments/seller<int:seller_id>/user<int:user_id>', methods=['GET', 'POST'])
def SellerReviews(seller_id, user_id):
    # get all reviews for a certain product:
    s_reviews = SellerReview.get_all_seller_reviews_for_seller_and_user(seller_id, user_id)
    # print(p_reviews, file=sys.stderr)
    review_comments = SR_Comment.get_all_seller_review_comments(seller_id, user_id)
    #p_r_avg = ProductReview.get_product_avg_rating(1)
    #product_review_stats = ProductReview.get_stats(product_number)

    seller_name = Seller.get_seller_info(seller_id)
    
    # render the page by adding information to the ProductReviews.html file
    return render_template('SRComments.html',
                            sellerreviews = s_reviews,
                            sellerreviewcomments = review_comments,
                            sellername = seller_name)


@bp.route('/sr_comments/seller<int:seller_id>/user<int:user_id>/upvote', methods=['GET', 'POST'])
def upvote(seller_id, user_id):
    SR_Comment.upvote_review(seller_id, user_id)
    return redirect(url_for('sr_comments.SellerReviews', seller_id = seller_id, user_id = user_id))

@bp.route('/sr_comments/seller<int:seller_id>/user<int:user_id>/downvote', methods=['GET', 'POST'])
def downvote(seller_id, user_id):
    SR_Comment.downvote_review(seller_id, user_id)
    return redirect(url_for('sr_comments.SellerReviews', seller_id = seller_id, user_id = user_id))

@bp.route('/sr_comments/seller<int:seller_id>/user<int:user_id>/upvote_comment/reviewer<int:reviewer_id>', methods=['GET', 'POST'])
def upvote_comment(seller_id, user_id, reviewer_id):
    SR_Comment.upvote_comment(seller_id, user_id, reviewer_id)
    return redirect(url_for('sr_comments.SellerReviews', seller_id = seller_id, user_id = user_id, reviewer_id = reviewer_id))

@bp.route('/sr_comments/seller<int:seller_id>/user<int:user_id>/downvote_comment/reviewer<int:reviewer_id>', methods=['GET', 'POST'])
def downvote_comment(seller_id, user_id, reviewer_id):
    SR_Comment.downvote_comment(seller_id, user_id, reviewer_id)
    return redirect(url_for('sr_comments.SellerReviews', seller_id = seller_id, user_id = user_id, reviewer_id = reviewer_id))