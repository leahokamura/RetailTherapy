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
 
from flask import Blueprint
bp = Blueprint('orderPage', __name__)


@bp.route('/orderPage', methods=['GET', 'POST'])
def orderPage():
    cart_items = Cart.get_cart(current_user.uid)
    return render_template('orderPage.html',items=cart_items)