import json

from flask import Response
from flask import request
from app import app
from flask_cors import CORS
from app.models.database import *
from flask_autodoc import Autodoc

CORS(app)
auto = Autodoc(app)


@app.route('/')
def index_reoute():
    return '/'


@app.route('/categories/<category_id>', methods=['GET'])
@auto.doc()
def return_categories(category_id):
    """
    Returns category and sub-categories
    """
    ret_data = get_categories(category_id)
    if ret_data is not None:
        response = Response(json.dumps(ret_data), status=200, mimetype='application/json')
        return response
    else:
        ret_data = 'Categories Not found'
        response = Response(json.dumps(ret_data), status=404, mimetype='application/json')
        return response


@app.route('/product')
@auto.doc()
def return_product():
    """
    Returns a product's complete information
    """
    asin_no = request.args.get('asin')
    category_id = request.args.get('categoryId')
    product = get_product(asin_no, category_id)

    product_dict = {
        "ASIN": product[0][0],
        "Title": product[0][1],
        "Price": product[0][2],
        "Link": product[0][3],
        "TotalReviews": product[0][4],
        "Score": product[0][5],
        "ImageLink": product[0][6],
        "Rate": product[0][7]
    }
    response = Response(json.dumps(product_dict), status=200, mimetype='application/json')
    return response


@app.route('/search-product/<keyword>', methods=['GET'])
@auto.doc()
def return_suggested_products(keyword):
    """
    Searches sub-strings in product labels in database and returns
    """
    res = search_product(keyword)
    response = Response(json.dumps(res), status=200, mimetype='application/json')
    return response


@app.route('/get-word-category/<product_id>', methods=['GET'])
@auto.doc()
def return_word_category(product_id):
    """
    Returns number of word count categories of product
    """
    word_categories = get_word_category(product_id)
    category_a = 0
    category_b = 0
    category_c = 0

    try:
        for category in word_categories:
            if category[0] == 'A':
                category_a += 1
            elif category[0] == 'B':
                category_b += 1
            elif category[0] == 'C':
                category_c += 1
            else:
                continue
    except Exception as e:
        print(e.message)

    res = {
        "A": category_a,
        "B": category_b,
        "C": category_c
    }

    response = Response(json.dumps(res), status=200, mimetype='application/json')
    return response


@app.route('/get-sentiment-label/<product_id>', methods=['GET'])
@auto.doc()
def return_sentiment_labels(product_id):
    """
    Returns total number of different sentiment label of product
    """
    labels = get_sentiment_label(product_id)
    labels_angry = 0
    labels_dissatisfied = 0
    labels_neutral = 0
    labels_staisfied = 0
    labels_happy = 0

    try:
        for label in labels:
            if label[0] == "angry":
                labels_angry += 1
            elif label[0] == "dissatisfied":
                labels_dissatisfied += 1
            elif label[0] == "neutral":
                labels_neutral += 1
            elif label[0] == "satisfied":
                labels_staisfied += 1
            elif label[0] == "happy":
                labels_happy += 1
            else:
                continue
    except Exception as e:
        print(e.message)

    res = {
        "Angry": labels_angry,
        "Dissatisfied": labels_dissatisfied,
        "Neutral": labels_neutral,
        "Satisfied": labels_staisfied,
        "Happy": labels_happy
    }

    response = Response(json.dumps(res), status=200, mimetype='application/json')
    return response


@app.route('/products/<category_id>', methods=['GET'])
@auto.doc()
def return_products(category_id):
    """
    Returns all products in a category
    """
    data_list = []
    if exists_category_in_db(category_id):
        ret_data = get_products(category_id)

        for product in ret_data:
            product_dict = {
                "ASIN": product[6],
                "Title": product[0],
                "Price": product[1],
                "Link": product[2],
                "ImageLink": product[5],
                "TotalReviews": product[3],
                "Score": product[4]
            }
            data_list.append(product_dict)

        if ret_data is not None:
            response = Response(json.dumps(data_list), status=200, mimetype='application/json')
            return response
        else:
            ret_data = 'Products Not Found !'
            response = Response(json.dumps(ret_data), status=404, mimetype='application/json')
            return response
    else:
        ret_data = 'Category {category} Not Found !'.format(category=category_id)
        response = Response(json.dumps(ret_data), status=404, mimetype='application/json')
        return response


@app.route('/docs')
def return_api_docs():
    return auto.html()
