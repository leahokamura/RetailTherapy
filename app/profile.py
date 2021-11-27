from __future__ import print_function # In python 2.7
from flask import render_template
from flask_login import current_user


from .models.user import User
from .models.seller import Seller

from flask import Blueprint
bp = Blueprint('profile', __name__)

@bp.route('/profile', methods=['GET', 'POST'])
def profile():
    #get profile info
    profile_info = User.get_profile(current_user.uid)
    # render the page by adding information to the profile.html file
    return render_template('profile.html', current_user = profile_info)

@bp.route('/seller')
def seller():
    print("ahhhhh i'm here")
    products = Seller.get_seller_products(current_user.uid)
    seller = Seller.get_seller_info(current_user.uid)
    # TODO: create seller.html
    return render_template('seller.html', slr=seller, inv=products)
