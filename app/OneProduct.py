from __future__ import print_function # In python 2.7
from flask import render_template
from flask_login import current_user

from app.models.productreview import ProductReview



# from .models.indproduct import OneProduct
from .models.product import Product
from .models.productreview import ProductReview

from flask import Blueprint

import sys
bp = Blueprint('oneproduct', __name__)

@bp.route('/oneproduct/<int:product_number>', methods=['GET', 'POST'])
def OneProducts(product_number):
    #get all info for a certain product
    print("this is the product number", product_number, file=sys.stderr)
    print(product_number, file=sys.stderr)
    p_info = Product.get(product_number)
    p_rating = ProductReview.get_just_rating(product_number)
    print("this is the product rating ", file=sys.stderr)
    print(p_rating, file=sys.stderr)
    print(p_info, file=sys.stderr)
    PR_check = True
    if current_user.is_authenticated:
        PR_check = ProductReview.review_check(product_number, current_user.uid)
    # render the page by adding information to the ind-product-page.html file
    return render_template('ind-product-page.html',
                            productinfo = p_info,
                            product_rating = p_rating,
                            productreviewcheck = PR_check)       