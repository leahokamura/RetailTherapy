from flask import render_template
from flask_login import current_user
import datetime

from .models.product import Product
from .models.purchase import Purchase
from .models.user import User

from flask import Blueprint
bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    # get all available products for sale:
    products = Product.get_all(True)
    # find the products current user has bought:
    # TO FIX: PURCHASES IS CURRENTLY BROKEN
    # if current_user.is_authenticated:
    #     purchases = Purchase.get_all_by_uid_since(
    #         current_user.uid, datetime.datetime(1980, 9, 14, 0, 0, 0))
    # else:
    purchases = None
    # render the page by adding information to the index.html file
    return render_template('index.html',
                           avail_products=products,
                           purchase_history=purchases)


@bp.route('/profile')
def profile():
    # get all profile info:
    profile = User.get_profile(True)
    # render the page by adding information to the profile.html file
    return render_template('profile.html',
                           current_user = profile)
