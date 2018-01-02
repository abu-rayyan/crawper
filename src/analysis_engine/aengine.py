import logging

from src.common.db.postgres_pool import PgPool
from config.config import QUERIES

logger = logging.getLogger(__name__)


class AEngine:
    def __init__(self):
        logger.debug('initiating AEngine')
        self.pg_pool = PgPool()

    def get_product_from_db(self, product_asin):
        logger.debug('getting product {asin} from database'.format(asin=product_asin))

        product_info = {
            "ASIN": None,
            "Title": None,
            "Price": None,
            "ReviewsURL": None,
            "Category": None,
            "URL": None,
            "TotalReviews": None
        }

        pg_conn, pg_cursor = self.pg_pool.get_conn()
        query = QUERIES["GetProduct"]
        params = (product_asin,)

        try:
            product = self.pg_pool.execute_query(pg_cursor, query, params)
            self.pg_pool.commit_changes(pg_conn)
            self.pg_pool.put_conn(pg_conn)

            product_info["ASIN"] = product[0][0]
            product_info["Title"] = product[0][1]
            product_info["Price"] = product[0][2]
            product_info["ReviewsURL"] = product[0][3]
            product_info["Category"] = product[0][4]
            product_info["URL"] = product[0][5]
            product_info["TotalReviews"] = product[0][6]

            return product_info

        except Exception as e:
            logger.exception(e.message)
            return None

    def get_product_reviews_from_db(self, product_asin):
        logger.debug('getting product {asin} reviews from database'.format(asin=product_asin))
        pg_conn, pg_cursor = self.pg_pool.get_conn()
        query = QUERIES["GetProductReviews"]
        params = (product_asin,)

        try:
            reviews = self.pg_pool.execute_query(pg_cursor, query, params)
            self.pg_pool.commit_changes(pg_conn)
            self.pg_pool.put_conn(pg_conn)
            return reviews
        except Exception as e:
            logger.debug(e.message)
            return None
