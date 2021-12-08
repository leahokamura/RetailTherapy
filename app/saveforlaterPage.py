from flask import render_template
from flask_login import current_user
import datetime

from .models.cart import Cart
from .models.saveforlater import Later

from flask import Blueprint
bp = Blueprint('saveforlaterPage', __name__)


@bp.route('/saveforlaterPage')
def saveforlaterPage():
    cart_items = Later.get_cart(current_user.uid)
    return render_template('SaveForLater.html', items=cart_items)

@bp.route('/addToCart/<int:pid><int:uid>', methods=['GET', 'POST'])
def addToCart(pid, uid):
    In = Later.check(pid, uid)

    if (In is True):
        print("It is in cart")

        message = '[Already in Save for Later]'
        cart_items = Cart.get_cart(uid)
        cart_total = Cart.get_total(uid)
        return render_template(('cart.html'), message = message, items=cart_items, total = cart_total)
    else: 
        print("not in cart")
        Later.add(pid, uid)
        Cart.remove(pid, uid)
        cart_items = Cart.get_cart(uid)
        cart_total = Cart.get_total(uid)
        return render_template(('cart.html'), message = message, items=cart_items, total = cart_total)




