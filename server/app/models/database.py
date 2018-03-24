from app.common.db.postgres import PgPool
from app.models.config.queries import QUERIES
from mock.categories import *

pg_ = PgPool()


def get_categories(category_id):
    """
    Returns categories/sub-categories to categories route
    :param category_id: id of category
    :return: list of categories/sub-categories
    """
    if category_id in Categories:
        return Categories[category_id]


def get_product(asin_no, category_id):
    """
    Returns a product information to product route
    :param asin_no: product asin
    :param category_id: id of category
    :return:
    """
    pg_conn, pg_cursor = pg_.get_conn()
    query = QUERIES["GetProduct"]
    params = (asin_no, category_id,)

    try:
        product_info = pg_.execute_query(pg_cursor, query, params)
        pg_.commit_changes(pg_conn)
        pg_.put_conn(pg_conn)
        return product_info
    except Exception as e:
        pg_.put_conn(pg_conn)
        return None


def get_products(category_id):
    """
    Returns all products of a category
    :param category_id: id of category
    :return:
    """
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


def search_product(keyword):
    """
    Searches and returns products info where the keyword in matched
    :param keyword:
    :return:
    """
    pg_conn, pg_cursor = pg_.get_conn()
    query = QUERIES["SearchProduct"]
    param = '%{key}%'.format(key=keyword)
    params = (param,)

    try:
        products = pg_.execute_query(pg_cursor, query, params)
        pg_.commit_changes(pg_conn)
        pg_.put_conn(pg_conn)
        return products
    except Exception as e:
        pg_.put_conn(pg_conn)
        return None


def exists_category_in_db(category_id):
    """
    Checks if a category exists in db
    :param category_id: id of category
    :return:
    """
    pg_conn, pg_cursor = pg_.get_conn()
    query = QUERIES["ExistsCategory"]
    params = (category_id,)

    try:
        res = pg_.execute_query(pg_cursor, query, params)
        pg_.commit_changes(pg_conn)
        pg_.put_conn(pg_conn)
        return res[0][0]
    except Exception as e:
        pg_.put_conn(pg_conn)  # TODO: generate exception logs here
        return None


def get_sentiment_label(product_id):
    """
    Returns sentiment labels of product
    :param product_id: id of product
    :return:
    """
    pg_conn, pg_cursor = pg_.get_conn()
    query = QUERIES["GetSentimentLabels"]
    params = (product_id,)

    try:
        res = pg_.execute_query(pg_cursor, query, params)
        pg_.commit_changes(pg_conn)
        pg_.put_conn(pg_conn)
        return res
    except Exception as e:
        pg_.put_conn(pg_conn)
        return None


def get_word_category(product_id):
    """
    Returns word count categories of product
    :param product_id: id of product
    :return:
    """
    pg_conn, pg_cursor = pg_.get_conn()
    query = QUERIES["GetWordCategory"]
    params = (product_id,)

    try:
        res = pg_.execute_query(pg_cursor, query, params)
        pg_.commit_changes(pg_conn)
        pg_.put_conn(pg_conn)
        return res
    except Exception as e:
        pg_.put_conn(pg_conn)
        return None

def get_credulity_score(product_id):
    """
    Returns word count categories of product
    :param product_id: id of product
    :return:
    """
    pg_conn, pg_cursor = pg_.get_conn()
    query = QUERIES["GetCredulityScoreOfProduct"]
    params = (product_id,)

    try:
        res = pg_.execute_query(pg_cursor, query, params)
        pg_.commit_changes(pg_conn)
        pg_.put_conn(pg_conn)
        return res
    except Exception as e:
        pg_.put_conn(pg_conn)
        return None

def sum_of_total_num_of_reviews():
    """

    :return:
    """
    pg_conn, pg_cursor = pg_.get_conn()
    query = QUERIES["Sum_of_total_num_of_reviews"]

    try:
        res = pg_.execute_query(pg_cursor, query, params='')
        pg_.commit_changes(pg_conn)
        pg_.put_conn(pg_conn)
        return res
    except Exception as e:
        pg_.put_conn(pg_conn)
        return None