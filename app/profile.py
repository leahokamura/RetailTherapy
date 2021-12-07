from __future__ import print_function # In python 2.7
from flask import render_template, flash, redirect, url_for
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, IntegerField, SelectField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, NumberRange
from flask_babel import _, lazy_gettext as _l


from .models.user import User
from .models.seller import Seller
from .models.account import Account
from .models.productreview import ProductReview
from .models.sellerreview import SellerReview
from .models.cart import Cart

from flask import Blueprint
bp = Blueprint('profile', __name__)

@bp.route('/profile', methods=['GET', 'POST'])
def profile():
    #get profile info
    profile_info = User.get_profile(current_user.uid)
    new_balance = Account.get_balance(current_user.uid)
    product_reviews = ProductReview.get_all_product_reviews_by_user(current_user.uid)
    seller_reviews = SellerReview.get_all_seller_reviews_by_user(current_user.uid)
    all_orders = Cart.get_cart(current_user.uid)
    # render the page by adding information to the profile.html file
    return render_template('profile.html', current_user = profile_info, 
                                            current_balance = new_balance,
                                            productreviews = product_reviews,
                                            sellerreviews = seller_reviews,
                                            orders = all_orders)

@bp.route('/profile/public', methods=['GET', 'POST'])
def public():
    #get public info
    public_info = User.get_public(current_user.uid)
    public_seller = User.get_public_seller(current_user.uid)
    # render the page by adding information to the public.html file
    return render_template('public.html', public_user = public_info, public_seller = public_seller)

@bp.route('/affirmations', methods=['GET', 'POST'])
def affirmations():
    # get profile info
    profile_info = User.get_profile(current_user.uid)
    # render the page by adding information to the affirmations.html file
    return render_template('affirmations.html', current_user = profile_info)

@bp.route('/seller')
def seller():
    User.make_seller(current_user.uid)
    products = Seller.get_seller_products(current_user.uid)
    seller = Seller.get_seller_info(current_user.uid)
    return render_template('seller.html', slr=seller, inv=products)

@bp.route('/seller/sort<sort_category>')
def sellersorted(sort_category=0):
    User.make_seller(current_user.uid)
    products = Seller.get_seller_products(current_user.uid)
    # print("sort category: ", sort_category)
    products = sorted(products, key=lambda x: x[int(sort_category)])
    # print("in order of", sort_category, products)
    seller = Seller.get_seller_info(current_user.uid)
    return render_template('seller.html', slr=seller, inv=products)

@bp.route('/seller/additem', methods=['GET', 'POST'])
def additem():
    form = AddToInventoryForm()
    form.category.choices = Seller.get_choices()
    if form.validate_on_submit():
        print('made it this far')
        if Seller.add_to_inventory(form.productname.data, form.price.data, form.quantity.data, form.description.data, form.image.data, form.category.data):
            return redirect(url_for('profile.seller'))
        else: 
            print('something hinky is going on')
    return render_template('additem.html', title='Add item', form=form)

class AddToInventoryForm(FlaskForm):
    productname = StringField(_l('Product Name'), validators=[DataRequired()])
    price = DecimalField(_l('Price'), validators=[DataRequired()]) # add: places = 2
    quantity = IntegerField(_l('Quantity Available'), validators=[NumberRange(min=0)])
    description = StringField(_l('Description (max 2048 characters)'), validators=[DataRequired()])
    image = StringField(_l('Image URL'), validators=[DataRequired()])
    category = SelectField(u'Category', validators=[DataRequired()])
    submit = SubmitField(_l('Add to Inventory'))   

@bp.route('/seller/edititem-<pid>-<pname>', methods=['GET', 'POST'])
def edititem(pid, pname):
    form = EditInventoryForm()
    form.productname.data = pname
    form.category.choices = Seller.get_choices()
    if form.validate_on_submit():
        print('made it this far')
        if Seller.edit_in_inventory(pid, form.productname.data, form.price.data, form.quantity.data, form.description.data, form.image.data, form.category.data):
            return redirect(url_for('profile.seller'))
        else: 
            print('something hinky is going on')
    return render_template('edititem.html', title='Edit item', form=form, pid=pid)

class EditInventoryForm(FlaskForm):
    productname = StringField(_l('Product Name'), validators=[DataRequired()])
    price = DecimalField(_l('Price'), validators=[DataRequired()]) # add: places = 2
    quantity = IntegerField(_l('Quantity Available'), validators=[NumberRange(min=0)])
    description = StringField(_l('Description (max 2048 characters)'), validators=[DataRequired()])
    image = StringField(_l('Image URL'), validators=[DataRequired()])
    category = SelectField(u'Category', validators=[DataRequired()])
    submit = SubmitField(_l('Save Changes'))

@bp.route('/seller/deleteitem-<pid>-<pname>', methods=['GET', 'POST'])
def deleteitem(pid, pname):
    return render_template('deleteitem.html', pid=pid, pname=pname)

@bp.route('/seller/deleteditem-<pid>')
def deleteditem(pid):
    print("pid:", pid)
    Seller.delete_from_inventory(pid)
    return render_template('deleteditem.html')
