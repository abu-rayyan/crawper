import json

from flask import Response
from server.app import app
from server.app.models.database import *
from server.app.models.common import find_item
from server.mock.categories import category_storage


@app.route('/')
def test():
    var = '3386071'
    return json.dumps(find_item(category_storage, var))


@app.route('/categories', methods=['GET'])
def return_categories():
    ret_data = get_categories()
    if ret_data is not None:
        response = Response(json.dumps(ret_data), status=200, mimetype='application/json')
        return response
    else:
        ret_data = 'Categories Not found'
        response = Response(json.dumps(ret_data), status=404, mimetype='application/json')
        return response


@app.route('/products/<category_name>', methods=['GET'])
def return_products(category_name):
    ret_data = get_products(category_name)
    if ret_data is not None:
        response = Response(json.dumps(ret_data), status=200, mimetype='application/json')
        return response
    else:
        ret_data = 'Category Not Found'
        response = Response(json.dumps(ret_data), status=400, mimetype='application/json')
        return response
