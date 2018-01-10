from __future__ import print_function
from server.app.common.db.postgres import PgPool
from server.app.models.config.queries import QUERIES

pg_ = PgPool()


def get_categories():
    print('getting categories from database')
    pg_conn, pg_cursor = pg_.get_conn()
    query = QUERIES["GetCategories"]

    try:
        categories = pg_.execute_query(pg_cursor, query, params='')
        pg_.commit_changes(pg_conn)
        pg_.put_conn(pg_conn)
        print(categories)
    except Exception as e:
        print(e.message)
        return None
