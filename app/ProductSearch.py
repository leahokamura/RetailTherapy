from __future__ import print_function # In python 2.7
from flask import render_template
from flask_login import current_user
from sqlalchemy.sql.elements import Null
from sqlalchemy.sql.expression import null, true

#import models
from .models.product import Product

from flask import Blueprint

import sys
bp = Blueprint('prodsearch', __name__)

#executes product search by category
# THIS ONE WORKED
# @bp.route('/prodsearch/<category>', methods=['GET', 'POST'])
# def ProductSearch(category):
#     print('this is the product category we are searching for', file=sys.stderr)
#     print(category, file=sys.stderr)
#     products = Product.get_prod_by_cat(category, sortCriteria='high', filterCriteria='none')
#     print(products, file=sys.stderr)
#     return render_template('prod-search.html',
#                             category = category,
#                             products = products, 
#                             category_search = 'true',
#                             sort_criteria = 'none',
#                             filter_criteria = 'none')

@bp.route('/prodsearch/<category>/<int:number>', methods=['GET', 'POST'])
def ProductSearch(category, number):
    print('this is the product category we are searching for', file=sys.stderr)
    print(category, file=sys.stderr)
    products = Product.get_prod_by_cat(category, number = number, sortCriteria='high', filterCriteria='none')
    
    total_num_prod = Product.get_total_prod_by_cat(category, sortCriteria='high', filterCriteria='none')
    print('this is total num prod in cat ', file=sys.stderr)
    print(total_num_prod, file=sys.stderr)
    
    print(products, file=sys.stderr)
    return render_template('prod-search.html',
                            category = category,
                            products = products, 
                            category_search = 'true',
                            sort_criteria = 'none',
                            filter_criteria = 'none',
                            number = number,
                            total = total_num_prod)

#executes product search by keyword
@bp.route('/keywordsearch/<keywords>/<int:number>', methods=['GET', 'POST'])
def ProductKeywordSearch(keywords, number):
    keywords_original = keywords
    keywords = keywords.strip()
    keywords = list(keywords.split(" "))

    keywords_adj = []
    for word in keywords:
        temp_word = '%' + word + '%'
        print(temp_word, file=sys.stderr)
        keywords_adj.append(temp_word)

    products = Product.get_by_keyword(keywords_adj, number=number, sortCriteria='low', filterCriteria='none')

    total_num_prod = Product.get_total_by_keyword(keywords_adj, sortCriteria='low', filterCriteria='none')
    print('this is total num prod with key ', file=sys.stderr)
    print(total_num_prod, file=sys.stderr)
    
    return render_template('prod-search.html',
                            category = keywords_original,
                            products = products, 
                            category_search = 'false',
                            sort_criteria = 'none',
                            filter_criteria = 'none',
                            number = number,
                            total = total_num_prod)

#executes sorting of search
@bp.route('/search/<keywords>/sort/<sortCriteria>/filter/<filterCriteria>/categorySearch/<category_search>/<int:number>', methods=['GET', 'POST'])
def FilterSort(keywords, sortCriteria, filterCriteria, category_search, number):
    if (category_search == 'true'):
        products = Product.get_prod_by_cat(keywords, sortCriteria, filterCriteria, number)
        total_num_prod = Product.get_total_prod_by_cat(keywords, sortCriteria='high', filterCriteria='none')

    else:
        keywords_arr = keywords.strip()
        keywords_arr = list(keywords.split(" "))
        keywords_adj = []
        
        for word in keywords_arr:
            temp_word = '%' + word + '%'
            keywords_adj.append(temp_word)
        
        total_num_prod = Product.get_total_by_keyword(keywords_adj, sortCriteria='low', filterCriteria='none')
        products = Product.get_by_keyword(keywords_adj, sortCriteria, filterCriteria, number)
    
    print("the filter criteria is " + filterCriteria, file=sys.stderr)
    if (filterCriteria == ''):
        print('filtering shuild be changed now ', file=sys.stderr)
        filterCriteria = 'none'
    
    if (sortCriteria == ''):
        print('sorting shuild be changed now ', file=sys.stderr)
        sortCriteria = 'none'

    # TO DO: will likely need to adjust this to include filter and sort criteria so as to allow both on results
    return render_template('prod-search.html',
                            category = keywords,
                            products = products,
                            category_search = category_search,
                            sort_criteria = sortCriteria,
                            filter_criteria = filterCriteria,
                            number = number,
                            total = total_num_prod)


# route used when filtering product results - pretty much the exact same as Sorting
# @bp.route('/search/<keywords>/sort/<sortCriteria>/filter/<filterCriteria>/categorySearch/<category_search>', methods=['GET', 'POST'])
# def Filtering(keywords, sortCriteria, filterCriteria, category_search):
#     if (category_search == 'true'):
#         products = Product.get_prod_by_cat(keywords, sortCriteria, filterCriteria)
#     else:
#         keywords_arr = keywords.strip()
#         keywords_arr = list(keywords.split(" "))
#         keywords_adj = []
        
#         for word in keywords_arr:
#             temp_word = '%' + word + '%'
#             keywords_adj.append(temp_word)
        
#         products = Product.get_by_keyword(keywords_adj, sortCriteria, filterCriteria)
    
#     print("the sort criteria is " + sortCriteria, file=sys.stderr)
#     if (sortCriteria == ''):
#         print('sorting shuild be changed now ', file=sys.stderr)
#         sortCriteria = 'none'
#     # TO DO: will likely need to adjust this to include filter and sort criteria so as to allow both on results
#     return render_template('prod-search.html',
#                             category = keywords,
#                             products = products,
#                             category_search = category_search,
#                             sort_criteria = sortCriteria,
#                             filter_Criteria = filterCriteria)