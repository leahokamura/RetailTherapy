from flask import render_template
from flask_login import current_user
import datetime

from .models.productreview import ProductReview

from flask import Blueprint
bp = Blueprint('productreviews', __name__)


@bp.route('/productreviews')
def ProductReviews():
    # get all reviews for a certain product:
    p_reviews = ProductReview.get_all_product_reviews_for_product(1)
    p_r_avg = ProductReview.get_product_avg_rating(1)
    
    # render the page by adding information to the ProductReviews.html file
    return render_template('ProductReviews.html',
                            productreviews = p_reviews,
                            avg_rating = p_r_avg)
