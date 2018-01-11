from server.app.common.db.postgres import PgPool
from server.app.models.config.queries import QUERIES
from server.mock.products import sports_outdoors
from server.mock.categories import categories

pg_ = PgPool()


def get_categories():
    return categories


def get_products(category_name):  # TODO: Get data from database instead of mock data
    if category_name == 'Sports Outdoors':
        return sports_outdoors
    else:
        return None
