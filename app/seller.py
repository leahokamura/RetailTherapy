from flask import render_template
from flask_login import current_user
import datetime

from .models.product import Product
from .models.purchase import Purchase
from .models.user import User
from .models.seller import Seller

from flask import Blueprint
bp = Blueprint('seller', __name__)

@bp.route('/seller/<int:uid>')
def seller(uid):
    print("ahhhhh i'm here")
    products = Seller.get_seller_products(uid)
    seller = Seller.get_seller_info(uid)
    print(seller)
    # TODO: create sellerpublic.html
    return render_template('sellerpublic.html', slr=seller, inv=products)