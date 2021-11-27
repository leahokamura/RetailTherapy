from flask import render_template
from flask_login import current_user
import datetime

from .models.product import Product
from .models.purchase import Purchase
from .models.user import User
from .models.seller import Seller

from flask import Blueprint
bp = Blueprint('seller', __name__)

# this is deprecated (i cannot figure out how to make it work, so it's been moved to profile.py)

@bp.route('/seller')
def seller():
    print("ahhhhh i'm here")
    products = Seller.get_seller_products(uid)
    seller = Seller.get_seller_info(uid)
    # TODO: create seller.html
    return render_template('seller.html', slr=seller, inv=products)