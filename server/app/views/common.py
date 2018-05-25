from __future__ import division
import json
from flask import Response
from flask import request
from app import app
from flask_cors import CORS
from app.models.database import *
from flask_autodoc import Autodoc
import math
import json

CORS(app)
auto = Autodoc(app)


@app.route('/')
def index_route():
    """
    Index route
    TODO: Need to handle it properly
    :return:
    """
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
    results = []
    res = search_product(keyword)
    for item in res:
        product = {
            "ASIN": item[0],
            "Title": item[1],
            "Price": item[2],
            "Score": item[3],
            "ImageLink": item[4],
            "Link": item[5],
            "CategoryId": item[6]
        }
        results.append(product)

    response = Response(json.dumps(results), status=200, mimetype='application/json')
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


@app.route('/get-credulity-score/<product_id>', methods=['GET'])
@auto.doc()
def return_credulity_score(product_id):
    """
    Returns credulity score of reviewer
    """
    credulity_score = get_credulity_score(product_id)
    credulity_1 = 0
    credulity_2 = 0
    credulity_3 = 0
    credulity_4 = 0
    credulity_5 = 0

    try:
        for score in credulity_score:
            if math.floor(score[0]) == 1:
                credulity_1 += 1
            elif math.floor(score[0]) == 2:
                credulity_2 += 1
            elif math.floor(score[0]) == 3:
                credulity_3 += 1
            elif math.floor(score[0]) == 4:
                credulity_4 += 1
            elif math.floor(score[0]) == 5:
                credulity_5 += 1
            else:
                continue
    except Exception as e:
        print(e.message)
    total_score = credulity_1+credulity_2+credulity_3+credulity_4+credulity_5

    res = [
        {
            'c1': (credulity_1/total_score)*100,
            'c2': (credulity_2/total_score)*100,
            'c3': (credulity_3/total_score)*100,
            'c4': (credulity_4/total_score)*100,
            'c5': (credulity_5/total_score)*100
    }
    ]

    response = Response(json.dumps(res), status=200, mimetype='application/json')
    return response


@app.route('/get-participation-history/<product_id>', methods=['GET'])
@auto.doc()
def return_participation_history(product_id):
    """
    Returns number of word count categories of product
    """
    participation_history = get_participation_history(product_id)
    r_1 = 0
    r_2 = 0
    r_3 = 0
    r_4 = 0
    r_5 = 0

    try:
        for p_h in participation_history:
            if p_h[0] == 'R1':
                r_1 += 1
            elif p_h[0] == 'R2':
                r_2 += 1
            elif p_h[0] == 'R3':
                r_3 += 1
            elif p_h[0] == 'R4':
                r_4 += 1
            elif p_h[0] == 'R5':
                r_5 += 1
            else:
                continue
    except Exception as e:
        print(e.message)
    total_score = r_1+r_2+r_3+r_4+r_5

    res = {
            'R1': (r_1/total_score)*100,
            'R2': (r_2/total_score)*100,
            'R3': (r_3/total_score)*100,
            'R4': (r_4/total_score)*100,
            'R5': (r_5/total_score)*100
    }

    response = Response(json.dumps(res), status=200, mimetype='application/json')
    return response


@app.route('/get-common-phrase/<product_id>', methods=['GET'])
@auto.doc()
def return_common_phrase(product_id):
    """
    Returns number of word count categories of product
    """
    common_phrase = get_common_phrase(product_id)

    cp_5 = 0
    cp_4 = 0
    cp_3 = 0
    cp_2 = 0
    cp_1 = 0

    try:
        for c_p in common_phrase:
            if c_p[0] == True and math.floor(c_p[1]) == 5.0:
                cp_5 += 1
            elif c_p[0] == True and math.floor(c_p[1]) == 4.0:
                cp_4 += 1
            elif c_p[0] == True and math.floor(c_p[1]) == 3.0:
                cp_3 += 1
            elif c_p[0] == True and math.floor(c_p[1]) == 2.0:
                cp_2 += 1
            elif c_p[0] == True and math.floor(c_p[1]) == 1.0:
                cp_1 += 1
            else:
                continue
    except Exception as e:
        print(e.message)

    res = {
            'r5': cp_5,
            'r4': cp_4,
            'r3': cp_3,
            'r2': cp_2,
            'r1': cp_1
    }

    response = Response(json.dumps(res), status=200, mimetype='application/json')
    return response


@app.route('/get-missing-middle/<product_id>', methods=['GET'])
@auto.doc()
def return_missing_middle(product_id):
    """
    Returns number of word count categories of product
    """
    middle_missing = get_missing_middle(product_id)

    star_1_2 = 0
    star_3 = 0
    star_4_5 = 0

    try:
        for m_m in middle_missing:
            if m_m[0] == 1:
                star_1_2 += 1
            elif m_m[0] == 2:
                star_1_2 += 1
            elif m_m[0] == 3:
                star_3 += 1
            elif m_m[0] == 4:
                star_4_5 += 1
            elif m_m[0] == 5:
                star_4_5 += 1
            else:
                continue
    except Exception as e:
        print(e.message)

    total = star_3 + star_1_2 + star_4_5

    if total == 0:
        return "There are no reviews related to this product"
    res = {
            'star1_2': (star_1_2/total)*100,
            'star3': (star_3/total)*100,
            'star4_5': (star_4_5/total)*100
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
        print(ret_data)

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


@app.route('/total-review-sum')
@auto.doc()
def return_sum_of_total_number_of_reviews():
    """
    Return sum of total number of reviews of products

    """
    sum_num_reviews = sum_of_total_num_of_reviews()
    s = 0
    for x in sum_num_reviews:
        for y in x:
            if ',' in y:
                y = y.replace(',', '')
            s = int(y) + s
    return str(s)


@app.route('/get-msdr/<product_id>', methods=['GET'])
@auto.doc()
def one_off_review_percentage(product_id):
    """
    Return percentage of one off review products

    """
    list_of_triggers = get_one_off_review_trigger(product_id)
    count = 0
    for trigger in list_of_triggers:
        print(trigger)
        if trigger[0]:
            count += 1
    if len(list_of_triggers) == 0:
        response = Response("Data is not available yet", status=200, mimetype='application/json' )
    else:
        one_off_percentage = (count/len(list_of_triggers))*100
        remaining = 100 - one_off_percentage
        res = {
            'ms': one_off_percentage,
            'rem': remaining
        }

        response = Response(json.dumps(res), status=200, mimetype='application/json')
    return response


@app.route('/get-multiple-single/<product_id>', methods=['GET'])
@auto.doc()
def multiple_single_day_review_percentage(product_id):
    """
    Return percentage of multiple single day review of products

    """
    list_of_triggers = get_multiple_single_day_review_trigger(product_id)
    count = 0
    for trigger in list_of_triggers:
        print(trigger)
        if trigger[0]:
            count += 1
    if len(list_of_triggers) == 0:
        response = Response("Data is not available", status=200, mimetype='application/json')
    else:
        one_off_percentage = (count/len(list_of_triggers))*100
        remaining = 100 - one_off_percentage
        res = {
            'msp': one_off_percentage,
            'remp': remaining
        }
        response = Response(json.dumps(res), status=200, mimetype='application/json')
    return response


@app.route('/detect-review-spikes/<product_id>', methods=['GET'])
@auto.doc()
def detection_of_review_spikes(product_id):

    review_spikes = get_review_spikes(product_id)
    list_review_data = []
    for rs in review_spikes:
        spikes = {
            "review_text": rs[0],
            "review_date": str(rs[1])
        }
        list_review_data.append(spikes)
    print list_review_data

    response = Response(json.dumps(list_review_data), status=200, mimetype='application/json')
    return response


@app.route('/rating_trend_rating_wise/<product_id>', methods=['GET'])
@auto.doc()
def rating_trend_rating_wise(product_id):
    l1 = []
    rating_trend = get_rating_using_date(product_id)
    print rating_trend
    for rating in rating_trend:
        avg_rate_per_date = {
           "avg_review": rating[0],
           "day": str(rating[1])
        }
        l1.append(avg_rate_per_date)
    print l1
    response = Response(json.dumps(l1), status=200, mimetype='application/json')
    return response


@app.route('/docs')
def return_api_docs():
    """
    api docs route
    :return:
    """
    return auto.html()