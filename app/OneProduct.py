from __future__ import print_function # In python 2.7
from flask import render_template
from flask_login import current_user



# from .models.indproduct import OneProduct
from .models.product import Product

from flask import Blueprint

import sys
bp = Blueprint('oneproduct', __name__)

@bp.route('/oneproduct')
def OneProducts():
    #get all info for a certain product
    p_info = Product.get(2)
    print(p_info, file=sys.stderr)
    # render the page by adding information to the ind-product-page.html file
    return render_template('ind-product-page.html',
                            productinfo = p_info)       