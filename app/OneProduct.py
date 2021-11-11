from __future__ import print_function # In python 2.7
from flask import render_template
from flask_login import current_user



# from .models.indproduct import OneProduct
from .models.product import Product

from flask import Blueprint

import sys
bp = Blueprint('oneproduct', __name__)

@bp.route('/oneproduct/<int:product_number>', methods=['GET', 'POST'])
def OneProducts(product_number):
    #get all info for a certain product
    print("this is the product number", file=sys.stderr)
    print(product_number, file=sys.stderr)
    p_info = Product.get(product_number)
    print(p_info, file=sys.stderr)
    # render the page by adding information to the ind-product-page.html file
    return render_template('ind-product-page.html',
                            productinfo = p_info)       