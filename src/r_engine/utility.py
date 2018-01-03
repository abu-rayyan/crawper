import logging

from config.config import QUERIES
from src.common.db.postgres_pool import PgPool

logger = logging.getLogger(__name__)


class UtilityFunctions:
    def __init__(self):
        logger.debug('initializing utility functions')
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

    def get_products_asin_from_db(self):
        logger.debug('getting all products asin from database')
        pg_conn, pg_cursor = self.pg_pool.get_conn()
        query = QUERIES["GetProductsAsin"]

        try:
            res_data = self.pg_pool.execute_query(pg_cursor, query, params='')
            self.pg_pool.commit_changes(pg_conn)
            self.pg_pool.put_conn(pg_conn)
            return res_data
        except Exception as e:
            logger.exception(e.message)
            return None

    def insert_rewiew_analysis_into_db(self, review_stat):
        logger.debug('inserting review analysis into database')
        pg_conn, pg_cursor = self.pg_pool.get_conn()
        query = QUERIES["InsertReviewStat"]
        params = (review_stat["ReviewLink"], review_stat["ReviewLength"],
                  review_stat["WordCountCategory"], review_stat["SentimentScore"],
                  review_stat["SentimentLabel"], review_stat["CommonPhrase"],
                  review_stat["CredulityScore"], review_stat["ReviewScore"])

        try:
            self.pg_pool.execute_query(pg_cursor, query, params)
            self.pg_pool.commit_changes(pg_conn)
            self.pg_pool.put_conn(pg_conn)
            return True
        except Exception as e:
            logger.exception(e.message)
            return False

    def get_reviewers_ids_from_db(self):
        logger.debug('getting reviewers information from database')
        pg_conn, pg_cursor = self.pg_pool.get_conn()
        query = QUERIES["GetReviewerIds"]

        try:
            reviewer_ids = self.pg_pool.execute_query(pg_cursor, query, params='')
            self.pg_pool.commit_changes(pg_conn)
            self.pg_pool.put_conn(pg_conn)
            return reviewer_ids
        except Exception as e:
            logger.exception(e.message)
            self.pg_pool.commit_changes(pg_conn)
            self.pg_pool.put_conn(pg_conn)
            return None

    def get_reviewers_total_reviews_from_db(self, reviewer_id):
        logger.debug('getting reviewer {id} total no of reviews  and ratings from database'.format(id=reviewer_id))
        pg_conn, pg_cursor = self.pg_pool.get_conn()
        query = QUERIES["GetTotalReviewsOfReviewer"]
        params = (reviewer_id,)

        try:
            reviews_rate = self.pg_pool.execute_query(pg_cursor, query, params)
            self.pg_pool.commit_changes(pg_conn)
            self.pg_pool.put_conn(pg_conn)
            return reviews_rate
        except Exception as e:
            logger.exception(e.message)
            self.pg_pool.commit_changes(pg_conn)
            self.pg_pool.put_conn(pg_conn)
            return None

    def update_reviewer_creduality_in_db(self, reviewer_data):
        logger.debug('updating reviewer {id} creduality score'.format(id=reviewer_data["ReviewerId"]))
        pg_conn, pg_cursor = self.pg_pool.get_conn()
        query = QUERIES["UpdateReviewerCredualityScore"]
        params = (reviewer_data["TotalReviews"], reviewer_data["CredualityScore"], reviewer_data["ReviewerId"])

        try:
            self.pg_pool.execute_query(pg_cursor, query, params)
            self.pg_pool.commit_changes(pg_conn)
            self.pg_pool.put_conn(pg_conn)
            return True
        except Exception as e:
            logger.exception(e.message)
            self.pg_pool.put_conn(pg_conn)
            return False

    def get_product_reviews_text_from_db(self, asin):
        logger.debug('getting product {asin} all reviews text from database'.format(asin=asin))
        pg_conn, pg_cursor = self.pg_pool.get_conn()
        query = QUERIES["GetProductReviewsText"]
        params = (asin,)

        try:
            reviews_text = self.pg_pool.execute_query(pg_cursor, query, params)
            self.pg_pool.commit_changes(pg_conn)
            self.pg_pool.put_conn(pg_conn)
            return reviews_text
        except Exception as e:
            logger.exception(e.message)
            self.pg_pool.put_conn(pg_conn)
            return None

    def get_reviewer_creduality_from_db(self, reviewer_id):
        logger.debug('getting reviewer {id} creaduality from database'.format(id=reviewer_id))
        pg_conn, pg_cursor = self.pg_pool.get_conn()
        query = QUERIES["GetReviewerCreaduality"]
        params = (reviewer_id,)

        try:
            creduality = self.pg_pool.execute_query(pg_cursor, query, params)
            self.pg_pool.commit_changes(pg_conn)
            self.pg_pool.put_conn(pg_conn)
            return creduality
        except Exception as e:
            logger.exception(e.message)
            self.pg_pool.put_conn(pg_conn)
            return None
