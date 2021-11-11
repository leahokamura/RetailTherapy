from __future__ import print_function # In python 2.7
from flask import render_template
from flask_login import current_user



from .models.user import User

from flask import Blueprint

import sys
bp = Blueprint('profile', __name__)

@bp.route('/profile/<int:uid>', methods=['GET', 'POST'])
def profile(uid):
    #get profile info
    print("this is your profile", file=sys.stderr)
    print(uid, file=sys.stderr)
    profile_info = User.get_profile(uid)
    print(profile_info, file=sys.stderr)
    # render the page by adding information to the profile.html file
    return render_template('profile.html',
                            current_user = profile_info) 