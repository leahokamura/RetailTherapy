from __future__ import print_function # In python 2.7
from flask import render_template, flash, redirect, url_for
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, IntegerField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, NumberRange
from flask_babel import _, lazy_gettext as _l


from .models.user import User
from .models.seller import Seller

from flask import Blueprint
bp = Blueprint('profile', __name__)

@bp.route('/profile', methods=['GET', 'POST'])
def profile():
    #get profile info
    profile_info = User.get_profile(current_user.uid)
    new_balance = User.get_balance(current_user.uid)
    # render the page by adding information to the profile.html file
    return render_template('profile.html', current_user = profile_info, current_balance = new_balance)

@bp.route('/public-profile/<int:uid>', methods=['GET', 'POST'])
def public():
    #get public info
    public_info = User.get_public(current_user.uid)
    public_seller = User.get_public_seller(current_user.uid)
    # render the page by adding information to the public.html file
    return render_template('public.html', public_user = public_info, public_seller = public_seller)

@bp.route('/seller')
def seller():
    User.make_seller(current_user.uid)
    products = Seller.get_seller_products(current_user.uid)
    seller = Seller.get_seller_info(current_user.uid)
    return render_template('seller.html', slr=seller, inv=products)

@bp.route('/seller/additem', methods=['GET', 'POST'])
def additem():
    form = AddToInventoryForm()
    if form.validate_on_submit():
        print('made it this far')
        if Seller.add_to_inventory(form.productname.data, form.price.data, form.quantity.data, form.description.data, form.image.data, form.category.data):
            return redirect(url_for('profile.seller'))
        else: 
            print('something hinky is going on')
    return render_template('additem.html', title='Add item', form=form)

class AddToInventoryForm(FlaskForm):
    productname = StringField(_l('Product name'), validators=[DataRequired()])
    price = DecimalField(_l('Price'), validators=[DataRequired()]) # add: places = 2
    quantity = IntegerField(_l('Quantity available'), validators=[NumberRange(min=0)])
    description = StringField(_l('Description (max 2048 characters)'), validators=[DataRequired()])
    image = StringField(_l('Image URL'), validators=[DataRequired()])
    category = StringField(_l('Category (Choose 1 from: drink, art, food)'))
    submit = SubmitField(_l('Add to inventory'))
