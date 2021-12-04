# from __future__ import print_function # In python 2.7
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
import datetime
import sys



from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, FloatField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, NumberRange
from flask_babel import _, lazy_gettext as _l


from .models.productreview import ProductReview
from .models.product import Product

from flask import current_app as app

from flask import Blueprint
# import sys
bp = Blueprint('addproductreviews', __name__)


class AddReviewForm(FlaskForm):
    rating = FloatField(_l('Rating'), validators=[DataRequired(), NumberRange(min=0, max=5)])
    comment = TextAreaField(_l('Comment'), validators=[DataRequired()])
    submit = SubmitField(_l('Add Review'))


@bp.route('/addproductreview/product<int:pid>/reviewer<int:rid>', methods=['GET', 'POST'])
def addProductReviews(pid, rid):
    if current_user.is_authenticated:
        form = AddReviewForm()
        print('check 1')
        if form.validate_on_submit():
            print('made it this far', file=sys.stderr)
            default_time = datetime.datetime.strptime('2001-01-10 14:12:58', '%Y-%m-%d %H:%M:%S')
            if ProductReview.addreview(rid,
                                        pid,
                                        default_time,
                                        form.rating.data,
                                        form.comment.data,
                                        0):
                print('made it into the if statement', file=sys.stderr)
                flash('Congratulations, you have submitted a review!')
                return redirect(url_for('ProductReviews.ProductReviews', product_number = pid))
            else:
                print('baddddd', file=sys.stderr)
    
    product_review_stats = ProductReview.get_stats(pid)

    product_name = Product.get_name(pid)
    return render_template('addproductreview.html', title='Add Product Review', 
                                                    form=form,
                                                    productname = product_name,
                                                    productreviewstats = product_review_stats)