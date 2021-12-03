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
    products = Product.get_prod_by_cat(category, sortCriteria='high', filterCriteria='none')
    print(products, file=sys.stderr)
    return render_template('prod-search.html',
                            category = category,
                            products = products, 
                            category_search = 'true')


@bp.route('/keywordsearch/<keywords>', methods=['GET', 'POST'])
def ProductKeywordSearch(keywords):
    keywords_original = keywords
    keywords = keywords.strip()
    keywords = list(keywords.split(" "))

    keywords_adj = []
    for word in keywords:
        temp_word = '%' + word + '%'
        print(temp_word, file=sys.stderr)
        keywords_adj.append(temp_word)

    products = Product.get_by_keyword(keywords_adj, sortCriteria='low', filterCriteria='none')

    return render_template('prod-search.html',
                            category = keywords_original,
                            products = products, 
                            category_search = 'false')


@bp.route('/search/<keywords>/sort/<sortCriteria>/categorySearch/<category_search>', methods=['GET', 'POST'])
def Sorting(keywords, sortCriteria, category_search):
    if (category_search == 'true'):
        products = Product.get_prod_by_cat(keywords, sortCriteria, 'none')
    else:
        keywords_arr = keywords.strip()
        keywords_arr = list(keywords.split(" "))
        keywords_adj = []
        
        for word in keywords_arr:
            temp_word = '%' + word + '%'
            keywords_adj.append(temp_word)
        
        products = Product.get_by_keyword(keywords_adj, sortCriteria, 'none')

    # TO DO: will likely need to adjust this to include filter and sort criteria so as to allow both on results
    return render_template('prod-search.html',
                            category = keywords,
                            products = products,
                            category_search = category_search)


# route used when filtering product results
@bp.route('/search/<keywords>/filter/<filterCriteria>/categorySearch/<category_search>', methods=['GET', 'POST'])
def Filtering(keywords, filterCriteria, category_search):
    if (category_search == 'true'):
        products = Product.get_prod_by_cat(keywords, 'none', filterCriteria)
    else:
        keywords_arr = keywords.strip()
        keywords_arr = list(keywords.split(" "))
        keywords_adj = []
        
        for word in keywords_arr:
            temp_word = '%' + word + '%'
            keywords_adj.append(temp_word)
        
        products = Product.get_by_keyword(keywords_adj, 'none', filterCriteria)
    
    # TO DO: will likely need to adjust this to include filter and sort criteria so as to allow both on results
    return render_template('prod-search.html',
                            category = keywords,
                            products = products,
                            category_search = category_search)