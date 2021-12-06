from __future__ import print_function # In python 2.7
from flask import render_template
from flask_login import current_user


from .models.user import User

from flask import Blueprint
bp = Blueprint('affirmations', __name__)


@bp.route('/affirmations', methods=['GET', 'POST'])
def affirmations():
    profile_info = User.get_profile(current_user.uid)
    return render_template('affirmations.html', current_user = profile_info)