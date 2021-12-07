from __future__ import print_function # In python 2.7
import sys
from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FloatField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, NumberRange
from flask_babel import _, lazy_gettext as _l
import random



from .models.user import User
from .models.affirm import Affirm

from flask import Blueprint
bp = Blueprint('affirmations', __name__)

class AffirmationForm(FlaskForm):
    affirmation = StringField(_l('Affirmation'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))

@bp.route('/affirmations', methods=['GET', 'POST'])
def affirmations():
    #get profile info
    profile_info = User.get_profile(current_user.uid)
    affirmations = Affirm.get_affirmations()
    # render the page by adding information to the profile.html file
    return render_template('affirmations.html', profile = profile_info, all_affirmations = affirmations)

@bp.route('/addaffirmation', methods=['GET', 'POST'])
def add():
    #form to add affirmation
    form = AffirmationForm()
    if form.validate_on_submit():
        Affirm.add_affirmation(form.affirmation.data)
        print('update worked')
        return redirect(url_for('affirmations.affirmations'))
    return render_template('addaffirmation.html', title='Add Affirmation', form=form)