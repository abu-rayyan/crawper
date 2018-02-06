import json

from flask import Response
from flask import request
from app import app
from flask_cors import CORS
from app.models.database import *

CORS(app)


@app.route('/')
def test():
    var = '3386071'
    return 'test route working'


@app.route('/categories/<category_id>', methods=['GET'])
def return_categories(category_id):
    ret_data = get_categories(category_id)
    if ret_data is not None:
        response = Response(json.dumps(ret_data), status=200, mimetype='application/json')
        return response
    else:
        ret_data = 'Categories Not found'
        response = Response(json.dumps(ret_data), status=404, mimetype='application/json')
        return response


@app.route('/product')
def return_product():
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
        "ImageLink": product[0][6]
    }
    response = Response(json.dumps(product_dict), status=200, mimetype='application/json')
    return response


@app.route('/search-product/<keyword>', methods=['GET'])
def return_suggested_products(keyword):
    res = search_product(keyword)
    response = Response(json.dumps(res), status=200, mimetype='application/json')
    return response


@app.route('/get-word-category/<product_id>', methods=['GET'])
def return_word_category(product_id):
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

    res = [
        {
            "Category": "A",
            "Count": category_a
         },
        {
            "Category": "B",
            "Count": category_b
        },
        {
            "Category": "C",
            "Count": category_c
        }
    ]
    response = Response(json.dumps(res), status=200, mimetype='application/json')
    return response


@app.route('/get-sentiment-label/<product_id>', methods=['GET'])
def return_sentiment_labels(product_id):
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

    res = [
        {
            "Label": "Angry",
            "Count": labels_angry
        },
        {
            "Label": "Dissatisfied",
            "Count": labels_dissatisfied
        },
        {
            "Label": "Neutral",
            "Count": labels_neutral
        },
        {
            "Label": "Satisfied",
            "Count": labels_staisfied
        },
        {
            "Label": "Happy",
            "Count": labels_happy
        }
    ]

    response = Response(json.dumps(res), status=200, mimetype='application/json')
    return response


@app.route('/products/<category_id>', methods=['GET'])
def return_products(category_id):
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
