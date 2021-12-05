# from __future__ import print_function # In python 2.7
from flask import render_template
from flask_login import current_user
import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, NumberRange


from .models.productreview import ProductReview
from .models.product import Product

from flask import current_app as app

from flask import Blueprint
# import sys
bp = Blueprint('productreviews', __name__)


@bp.route('/productreviews/<int:product_number>', methods=['GET', 'POST'])
def ProductReviews(product_number):
    # get all reviews for a certain product:
    p_reviews = ProductReview.get_all_product_reviews_for_product(product_number)
    # print(p_reviews, file=sys.stderr)

    #p_r_avg = ProductReview.get_product_avg_rating(1)
    product_review_stats = ProductReview.get_stats(product_number)

    product_name = Product.get_name(product_number)

    PR_check = ProductReview.review_check(product_number, current_user.uid)
    
    # render the page by adding information to the ProductReviews.html file
    return render_template('ProductReviews.html',
                            productreviews = p_reviews,
                            productreviewstats = product_review_stats,
                            productname = product_name,
                            productreviewcheck = PR_check)
                            #avg_rating = p_r_avg)

