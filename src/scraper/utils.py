import logging

from config.config import *
from src.common.db.postgres_pool import PgPool

logger = logging.getLogger(__name__)


class Utils:
    def __init__(self):
        logger.debug('initiating scraper utils')
        self.pg_ = PgPool()

    def insert_product_into_db(self, product, category_id):
        """
        Inserts product's information to database
        :param product: product info dictionary
        :param category_id: category id
        :return: bool
        """
        logger.debug('inserting product {asin} into database'.format(asin=product["ASIN"]))
        pg_conn, pg_cursor = self.pg_.get_conn()
        query = QUERIES["InsertProduct"]
        params = (product["ASIN"], product["Title"], product["Price"], product["ReviewsURL"],
                  category_id, product["ProductLink"], product["TotalReviews"], '0', product["ImageLink"],
                  product["Rating"],)

        try:
            self.pg_.execute_query(pg_cursor, query, params)
            self.pg_.commit_changes(pg_conn)
            self.pg_.put_conn(pg_conn)
            return True
        except Exception as e:
            logger.exception(e.message)
            return False

    def insert_review_into_db(self, review, product_asin):
        """
        Inserts review to the database
        :param review: review dictionary
        :param product_asin: asin number of product
        :return: bool
        """
        logger.debug('inserting review {id} into database'.format(id=review["ReviewLink"]))
        pg_conn, pg_cursor = self.pg_.get_conn()
        query = QUERIES["InsertReview"]
        params = (review["ReviewLink"], product_asin,
                  review["ReviewTitle"], review["ReviewText"],
                  review["ReviewerId"], review["ReviewDate"],
                  review["ReviewRate"],)

        try:
            self.pg_.execute_query(pg_cursor, query, params)
            self.pg_.commit_changes(pg_conn)
            self.pg_.put_conn(pg_conn)
            return True
        except Exception as e:
            logger.exception(e.message)
            self.pg_.put_conn(pg_conn)
            return False

    def exists_product_in_db(self, product_asin):
        """
        Checks if a product already exists in the database
        :param product_asin: asin no of product
        :return: bool
        """
        logger.debug('checking if product {asin} exists in database'.format(asin=product_asin))
        pg_conn, pg_cursor = self.pg_.get_conn()
        query = QUERIES["ProductExists"]
        params = (product_asin,)

        try:
            success_bool = self.pg_.execute_query(pg_cursor, query, params)
            self.pg_.commit_changes(pg_conn)
            self.pg_.put_conn(pg_conn)
            return success_bool[0][0]
        except Exception as e:
            logger.exception(e.message)
            self.pg_.put_conn(pg_conn)
            return None

    def exists_reviewer_in_db(self, reviewer_id):
        """
        Checks if reviewer already exists in database
        :param reviewer_id: reviewer id
        :return: bool
        """
        logger.debug('checking if reviewer {id} exists in database'.format(id=reviewer_id))
        pg_conn, pg_cursor = self.pg_.get_conn()
        query = QUERIES["ReviewerExists"]
        params = (reviewer_id,)

        try:
            success_bool = self.pg_.execute_query(pg_cursor, query, params)
            self.pg_.commit_changes(pg_conn)
            self.pg_.put_conn(pg_conn)
            return success_bool[0][0]
        except Exception as e:
            logger.exception(e.message)
            return None

    def insert_reviewer_into_db(self, review):
        """
        Inserts reviewer's information to database
        :param review: review dictionary
        :return: bool
        """
        if not self.exists_reviewer_in_db(review["ReviewerId"]):
            logger.debug('reviewer not exists in db, inserting reviewer {id} into database'.format(
                id=review["ReviewerId"]))
            pg_conn, pg_cursor = self.pg_.get_conn()
            query = QUERIES["InsertReviewer"]
            params = (review["ReviewerId"], review["ReviewerName"], review["ReviewerProfile"], 0, 0.0,)

            try:
                self.pg_.execute_query(pg_cursor, query, params)
                self.pg_.commit_changes(pg_conn)
                self.pg_.put_conn(pg_conn)
                return True
            except Exception as e:
                logger.exception(e.message)
                return False
        else:
            logger.debug('reviewer {id} already exists in database'.format(id=review["ReviewerId"]))

    def exists_review_in_db(self, review_link):
        """
        Checks if a review exists in the database
        :param review_link: review URL TODO: use review id instead
        :return: bool
        """
        logger.debug('checking if review {link} exists in the database'.format(link=review_link))
        pg_conn, pg_cursor = self.pg_.get_conn()
        query = QUERIES["ExistsReview"]
        params = (review_link,)

        try:
            success_bool = self.pg_.execute_query(pg_cursor, query, params)
            self.pg_.commit_changes(pg_conn)
            self.pg_.put_conn(pg_conn)
            return success_bool[0][0]
        except Exception as e:
            logger.exception(e.message)
            return None
