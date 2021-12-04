from flask import render_template
from flask import current_app as app
from flask_login import current_user
import datetime

from .models.product import Product
from .models.purchase import Purchase
from .models.user import User
from .models.seller import Seller

from flask import Blueprint
bp = Blueprint('sellers', __name__)

@bp.route('/sellers')
def sellers():
    print("ahhhhh i'm here")
    rows = app.db.execute(
        """
        SELECT Sellers.uid AS sid, Users.firstname AS firstname, Users.lastname AS lastname, Users.email AS email
        FROM Sellers, Users
        WHERE Sellers.uid = Users.uid
        """
    )
    # TODO: create sellers.html
    return render_template('sellers.html', slrs=[row for row in rows])