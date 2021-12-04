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

@bp.route('/public-profile', methods=['GET', 'POST'])
def public():
    #get public info
    public_info = User.get_public(current_user.uid)
    # render the page by adding information to the public.html file
    return render_template('public.html', public_user = public_info)

@bp.route('/seller')
def seller():
    User.make_seller(current_user.uid)
    products = Seller.get_seller_products(current_user.uid)
    seller = Seller.get_seller_info(current_user.uid)
    return render_template('seller.html', slr=seller, inv=products)

@bp.route('/public-profile-seller', methods=['GET', 'POST'])
def public_seller():
    #get public info
    public_info = User.get_public_seller(current_user.uid)
    # render the page by adding information to the public.html file
    return render_template('public.html', public_user = public_info)
