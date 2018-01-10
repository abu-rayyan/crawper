import json

from server.app import app
from server.app.models.database import *

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
    get_categories()
    return "sdjhaskjhdasjkhdahskjdhlkash"
