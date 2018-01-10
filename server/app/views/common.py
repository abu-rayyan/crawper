from flask import request
from server.app import app
from server.app.models import common


@app.route('/test')
def test():
    return common.MESSAGES["Test"]
