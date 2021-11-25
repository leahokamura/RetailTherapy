from __future__ import print_function # In python 2.7
from flask import render_template
from flask_login import current_user
from sqlalchemy.sql.elements import Null
from sqlalchemy.sql.expression import null, true

from .models.product import Product

from flask import Blueprint

import sys
bp = Blueprint('prodsearch', __name__)

@bp.route('/prodsearch/<category>', methods=['GET', 'POST'])
def ProductSearch(category):
    print('this is the product category we are searching for', file=sys.stderr)
    print(category, file=sys.stderr)
    products = Product.get_prod_by_cat(category, sortCriteria='high')
    print(products, file=sys.stderr)
    return render_template('prod-search.html',
                            category = category,
                            products = products, 
                            category_search = 'true')

@bp.route('/keywordsearch/<keywords>', methods=['GET', 'POST'])
def ProductKeywordSearch(keywords):
    print('these are the keywords that we are searching for', file=sys.stderr)
    print(keywords, file=sys.stderr)
    keywords_original = keywords
    keywords = keywords.strip()
    keywords = list(keywords.split(" "))
    print('these are the keywords that we are searching for again', file=sys.stderr)
    print(keywords, file=sys.stderr)
    keywords_adj = []
    for word in keywords:
        temp_word = '%' + word + '%'
        print(temp_word, file=sys.stderr)
        keywords_adj.append(temp_word)
    print('these are the adjusted keywords ', file=sys.stderr)
    print(keywords_adj, file=sys.stderr)
    # products = []
    # prod_ids = []
    # for word in keywords:
    #     tempList = Product.get_by_keyword(word)
    #     if tempList is not None:
    #         for prod in tempList:
    #             print('this is the product in question', file=sys.stderr)
    #             print(prod.pid, file = sys.stderr)
    #             if prod.pid not in prod_ids:
    #                 products.append(prod)
    #                 prod_ids.append(prod.pid)
    products = Product.get_by_keyword(keywords_adj, sortCriteria='low')
    print('these are the products ', file=sys.stderr)
    print(products, file=sys.stderr)
    return render_template('prod-search.html',
                            category = keywords_original,
                            products = products, 
                            category_search = 'false')

@bp.route('/search/<keywords>/sort/<sortCriteria>/categorySearch/<category_search>', methods=['GET', 'POST'])
def PriceSort(keywords, sortCriteria, category_search):
    print('this is a category search', file=sys.stderr)
    print(category_search, file=sys.stderr)
    print('these are the original search terms', file=sys.stderr)
    print(keywords, file=sys.stderr)
    print('this is the sort criteria', file=sys.stderr)
    print(sortCriteria, file=sys.stderr)
    
    if (category_search == 'true'):
        print('start here', file=sys.stderr)
        products = Product.get_prod_by_cat(keywords, sortCriteria)
        print('end here', file=sys.stderr)
    else:
        keywords_arr = keywords.strip()
        keywords_arr = list(keywords.split(" "))
        keywords_adj = []
        for word in keywords_arr:
            temp_word = '%' + word + '%'
            print(temp_word, file=sys.stderr)
            keywords_adj.append(temp_word)
        print('made it here', file=sys.stderr)
        products = Product.get_by_keyword(keywords_adj, sortCriteria)
        print('made it to end', file=sys.stderr)

    

    print("FUCKING HELL ", file=sys.stderr)

    # products.sort(key=Product.name, reverse=True)
    print("these are the products ", file=sys.stderr)
    print(products, file=sys.stderr)
    return render_template('prod-search.html',
                            category = keywords,
                            products = products,
                            category_search = category_search)
