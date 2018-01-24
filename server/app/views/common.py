import json

from flask import Response
from server.app import app
from flask_cors import CORS
from server.app.models.database import *

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


@app.route('/products/<category_id>', methods=['GET'])
def return_products(category_id):
    data_list = []
    if exists_category_in_db(category_id):
        ret_data = get_products(category_id)

        for product in ret_data:
            product_dict = {
                "Title": product[0],
                "Price": product[1],
                "Link": product[2],
                "Image Link": product[5],
                "Total Reviews": product[3],
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
