from __future__ import print_function # In python 2.7
import sys
from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import _, lazy_gettext as _l

from .models.user import User
from .models.product import Product
from .models.cart import Cart
from .models.order_checkout import Order
import datetime
 
from flask import Blueprint
bp = Blueprint('orderPage', __name__)


@bp.route('/orderPage', methods=['GET', 'POST'])
def orderPage():
    cart_items = Cart.get_cart(current_user.uid)
    cart_total = Cart.get_total(current_user.uid)
    default_time = datetime.datetime.now()
    default_time = datetime.datetime.strftime(default_time, '%Y-%m-%d %H:%M:%S')
    user_balance = Order.get_balance(current_user.uid)
    
    if cart_total > user_balance:
        #this flash is not working yet :(
        print('Insufficient Balance')
        return redirect(url_for('cart.cart'))

    placed_order = Order.inventory_check(cart_items)
    if placed_order == False:
        #this flash is not working yet :(
        print('Insufficient Stock')
        return redirect(url_for('cart.cart'))

    Order.addToOrders(current_user.uid, cart_total, default_time)
    Order.update_stock(cart_items)
    Order.update_balances(cart_items, current_user.uid, cart_total)
    Order.empty_cart(cart_items, current_user.uid)
    status = "Not Fulfilled"
    
    return render_template('orderPage.html',items=cart_items, total = cart_total, status = status)