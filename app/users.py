from __future__ import print_function # In python 2.7
import sys
from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FloatField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, NumberRange
from flask_babel import _, lazy_gettext as _l

from .models.user import User
from .models.product import Product
from .models.cart import Cart
from .models.account import Account

from flask import Blueprint
bp = Blueprint('users', __name__)


class LoginForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Remember Me'))
    submit = SubmitField(_l('Sign In'))


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_auth(form.email.data, form.password.data)
        if user is None:
            flash('Invalid email or password')
            return redirect(url_for('users.login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index.index')

        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


class RegistrationForm(FlaskForm):
    firstname = StringField(_l('First Name'), validators=[DataRequired()])
    lastname = StringField(_l('Last Name'), validators=[DataRequired()])
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _l('Repeat Password'), validators=[DataRequired(),
                                           EqualTo('password')])
    submit = SubmitField(_l('Register'))

    def validate_email(self, email):
        if User.email_exists(email.data):
            raise ValidationError(_('Already a user with this email.'))


class UpdateProfile(FlaskForm):
    firstname = StringField(_l('First Name'), validators=[DataRequired()])
    lastname = StringField(_l('Last Name'), validators=[DataRequired()])
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _l('Repeat Password'), validators=[DataRequired(), EqualTo('password')])
    address = StringField(_l('Address'))
    submit = SubmitField(_l('Update Profile'))

    def validate_email_update(self, email):
        if User.email_exists_update(email.data, self.uid):
            raise ValidationError(_('Already a user with this email.'))

class UpdateBalance(FlaskForm):
    balance = FloatField(_l('Balance'), validators=[DataRequired()])
    submit = SubmitField(_l('Update Balance'))

    def validate_balance(self, balance):
        if self.balance.data + balance.data < 0.0:
            raise ValidationError(_('Insufficient funds.'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        print('made it this far', file=sys.stderr)
        if User.register(form.email.data,
                         form.password.data,
                         form.firstname.data,
                         form.lastname.data):
            #flash('Congratulations, you are now a registered user!')
            return redirect(url_for('users.login'))
        else: 
            print('something fucked up', file=sys.stderr)
    return render_template('register.html', title='Register', form=form)


@bp.route('/update', methods=['GET', 'POST'])
def update():
    form = UpdateProfile()
    if request.method == 'POST':
        if form.validate_on_submit():
            User.update_profile(current_user.uid,
                    form.email.data, 
                    form.password.data,
                    form.firstname.data,
                    form.lastname.data,
                    form.address.data) 
            #flash('Congratulations, you have updated your profile information!')
            return redirect(url_for('profile.profile'))                    
        return render_template('update.html', title='Update Profile', form=form)
    else:
        form.email.data = current_user.email
        form.password.data = current_user.password
        form.firstname.data = current_user.firstname
        form.lastname.data = current_user.lastname
        form.address.data = current_user.address
        return render_template('update.html', title='Update Profile', form=form)

@bp.route('/update-balance', methods=['GET', 'POST'])
def updateBalance():
    form = UpdateBalance()
    if request.method == 'POST':
        if form.validate_on_submit():
            if Account.update_balance(current_user.uid, form.balance.data):
                #flash('Congratulations, you have updated your balance!')
                print('update worked')
                print(form.balance.data)
                x = Account.get_balance(current_user.uid)
                y = Account.update_balance(current_user.uid, form.balance.data)
                print(x)
                print(y)
                return redirect(url_for('profile.profile'))                
    return render_template('balance.html', title='Update Balance', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index.index'))
     
     #Leah is working on this :/
@bp.route('/addToCart/<int:pid><int:uid>', methods=['GET', 'POST'])
def addToCart(pid, uid):
    In = Cart.check(pid, uid)
    if (In is True):
        print("It is in cart")
        Cart.update(pid, uid, 'add')
    else: 
        print("not in cart")
        Cart.add(pid, uid)
    return redirect(url_for('index.index'))

@bp.route('/remove_item/<int:pid><int:uid>', methods=['GET', 'POST'])
def remove_item(pid, uid):
    Cart.remove(pid, uid)
    print("removed item")
    return redirect(url_for('cart.cart'))

@bp.route('/Add/<int:pid><int:uid>', methods=['GET', 'POST'])
def Add(pid, uid):
    Cart.update(pid, uid, 'add')
    return redirect(url_for('cart.cart'))

@bp.route('/removeOne/<int:pid><int:uid>', methods=['GET', 'POST'])
def removeOne(pid, uid):
    Cart.update(pid, uid, 'delete')
    # quantity_zero = Cart.check_ifZero(pid,uid)
    # if (quantity_zero is True):
    #     Cart.remove(pid, uid)
    return redirect(url_for('cart.cart'))
