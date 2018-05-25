# noinspection PyUnresolvedReferences,PyUnresolvedReferences,PyUnresolvedReferences,PyUnresolvedReferences,PyUnresolvedReferences
from app.common.db.postgres import PgPool
import random

pg_ = PgPool()
def get_data():
    pg_conn, pg_cursor = pg_.get_conn()
    query = "SELECT product_asin FROM crawper.products;"

    try:
        product_id = pg_.execute_query(pg_cursor, query, params="")
        pg_.commit_changes(pg_conn)
        pg_.put_conn(pg_conn)
        update_product(product_id)
        return product_id
    except Exception as e:
        pg_.put_conn(pg_conn)
        return None

def update_product(product_id):
    pg_conn, pg_cursor = pg_.get_conn()
    query = "UPDATE crawper.products SET msdr=%s WHERE reviewer_id=%s;"

    try:
        for x in product_id:
            msgr_rand = random.randint(1, 6)
            params = (msgr_rand, x,)
            pg_.execute_query(pg_cursor, query, params)
            pg_.commit_changes(pg_conn)

        return True
    except Exception as e:
        pg_.put_conn(pg_conn)
        return False