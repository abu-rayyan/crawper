from server.app.common.db.postgres import PgPool
from server.app.models.config.queries import QUERIES
from server.mock.categories import *

pg_ = PgPool()


def get_categories(category_id):
    if category_id in Categories:
        return Categories[category_id]


def get_products(category_id):
    pg_conn, pg_cursor = pg_.get_conn()
    query = QUERIES["GetCategoryProducts"]
    params = (category_id,)

    try:
        product_list = pg_.execute_query(pg_cursor, query, params)
        pg_.commit_changes(pg_conn)
        pg_.put_conn(pg_conn)
        return product_list
    except Exception as e:
        pg_.put_conn(pg_conn)  # TODO: use logger here
        return None


def exists_category_in_db(category_name):
    pg_conn, pg_cursor = pg_.get_conn()
    query = QUERIES["ExistsCategory"]
    params = (category_name,)

    try:
        res = pg_.execute_query(pg_cursor, query, params)
        pg_.commit_changes(pg_conn)
        pg_.put_conn(pg_conn)
        return res[0][0]
    except Exception as e:
        pg_.put_conn(pg_conn)  # TODO: generate exception logs here
        return None
