from __future__ import print_function # In python 2.7
from flask import render_template
from flask_login import current_user
from sqlalchemy.sql.elements import Null
from sqlalchemy.sql.expression import null

from .models.product import Product

from flask import Blueprint

import sys
bp = Blueprint('prodsearch', __name__)

@bp.route('/prodsearch/<category>', methods=['GET', 'POST'])
def ProductSearch(category):
    print('this is the product category we are searching for', file=sys.stderr)
    print(category, file=sys.stderr)
    products = Product.get_prod_by_cat(category)
    print(products, file=sys.stderr)
    return render_template('prod-search.html',
                            category = category,
                            products = products)

@bp.route('/keywordsearch/<keywords>', methods=['GET', 'POST'])
def ProductKeywordSearch(keywords):
    print('these are the keywords that we are searching for', file=sys.stderr)
    print(keywords, file=sys.stderr)
    keywords_original = keywords
    keywords = keywords.strip()
    keywords = list(keywords.split(" "))
    print('these are the keywords that we are searching for again', file=sys.stderr)
    print(keywords, file=sys.stderr)
    
    products = []
    prod_ids = []
    for word in keywords:
        tempList = Product.get_by_keyword(word)
        if tempList is not None:
            for prod in tempList:
                print('this is the product in question', file=sys.stderr)
                print(prod.pid, file = sys.stderr)
                if prod.pid not in prod_ids:
                    products.append(prod)
                    prod_ids.append(prod.pid)
    # products = Product.get_by_keyword(keywords)
    print('these are the products ', file=sys.stderr)
    print(products, file=sys.stderr)
    return render_template('prod-search.html',
                            category = keywords_original,
                            products = products)