from flask import render_template
from flask_login import current_user
import datetime

from .models.productreview import ProductReviews

from flask import Blueprint
bp = Blueprint('ProductReviews', __name__)


@bp.route('/ProductReviews')
def ProductReviews():
    # get all reviews for a certain product:
    productreviews = Product.get_all_product_reviews_for_product(pid)
    
    # render the page by adding information to the ProductReviews.html file
    return render_template('ProductReviews.html',
                           Product_Reviews = productreviews)
