# from __future__ import print_function # In python 2.7
from flask import render_template
from flask_login import current_user
import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, NumberRange


from .models.sellerreview import SellerReview
from .models.seller import Seller

from flask import current_app as app

from flask import Blueprint
# import sys
bp = Blueprint('sellerreviews', __name__)


@bp.route('/sellerreviews/<int:seller_id>', methods=['GET', 'POST'])
def SellerReviews(seller_id):
    # get all reviews for a certain product:
    s_reviews = SellerReview.get_all_seller_reviews_for_seller(seller_id)
    # print(p_reviews, file=sys.stderr)

    #p_r_avg = ProductReview.get_product_avg_rating(1)
    seller_review_stats = SellerReview.get_stats(seller_id)

    seller_name = Seller.get_seller_info(seller_id)
    
    # render the page by adding information to the ProductReviews.html file
    return render_template('sellerreviews.html',
                            sellerreviews = s_reviews,
                            sellerreviewstats = seller_review_stats,
                            sellername = seller_name)
                            #avg_rating = p_r_avg)