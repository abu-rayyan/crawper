import json

from flask import request
from server.app import app
from server.app.models import common

var = [{
    "Categories": {
        "Sports & Outdoors": {
            "Fan Shop": {
                "Auto Accessories": {
                    "Air Fresheners": {},
                    "Antenna Toppers": {},
                    "Car Covers": {}
                },
                "Bags, Packs & Accessories": {}

            },
            "Outdoor Recreation": {},
            "Sports & Fitness": {}
        }
    }
}]


@app.route('/')
def test():
    return "Crawper Server routes working"


@app.route('/categories')
def return_categories():
    return json.dumps(var)
