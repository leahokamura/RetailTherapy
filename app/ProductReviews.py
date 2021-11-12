# from __future__ import print_function # In python 2.7
from flask import render_template
from flask_login import current_user
import datetime

from .models.productreview import ProductReview

from flask import current_app as app

from flask import Blueprint
# import sys
bp = Blueprint('productreviews', __name__)


# @bp.route('/productreviews')
# def ProductReviews():
#     # get all reviews for a certain product:
#     p_reviews = ProductReview.get_all_product_reviews_for_product(1)
#     # print(p_reviews, file=sys.stderr)

#     #p_r_avg = ProductReview.get_product_avg_rating(1)
#     product_review_stats = ProductReview.get_stats(1)
    
#     # render the page by adding information to the ProductReviews.html file
#     return render_template('ProductReviews.html',
#                             productreviews = p_reviews,
#                             productreviewstats = product_review_stats)
#                             #avg_rating = p_r_avg)

@bp.route('/productreviews/<int:product_number>', methods=['GET', 'POST'])
def ProductReviews(product_number):
    # get all reviews for a certain product:
    p_reviews = ProductReview.get_all_product_reviews_for_product(product_number)
    # print(p_reviews, file=sys.stderr)

    #p_r_avg = ProductReview.get_product_avg_rating(1)
    product_review_stats = ProductReview.get_stats(product_number)

    product_name = app.db.execute(
        """
        SELECT name
        FROM Products, Product_Reviews
        WHERE Products.pid = Product_Reviews.pid
        """
    )[product_number][0]
    
    # render the page by adding information to the ProductReviews.html file
    return render_template('ProductReviews.html',
                            productreviews = p_reviews,
                            productreviewstats = product_review_stats,
                            productname = product_name)
                            #avg_rating = p_r_avg)