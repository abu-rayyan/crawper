import logging

from config.config import *

logger = logging.getLogger(__name__)


# Utility methods for crawler
class Utils:
    def __init__(self, conn, cursor, pool):
        logger.debug('initiating crawler utils')
        self.pg_ = pool
        self.pg_conn = conn
        self.pg_cursor = cursor

    def get_no_of_scraped_reviews_from_db(self, product_asin):
        """
        Returns total number of scraped reviews of a product
        :param product_asin: asin number of product
        :return: no of scraped reviews
        """
        logger.debug('getting product {asin} total no of scraped reviews from database'.format(
            asin=product_asin))
        query = QUERIES["GetProductReviewCount"]
        params = (product_asin,)

        try:
            reviews_count = self.pg_.execute_query(self.pg_cursor, query, params)[0][0]
            self.pg_.commit_changes(self.pg_conn)
            return reviews_count
        except Exception as e:
            logger.exception(e.message)
            return None

    def exists_product_in_db(self, product_asin):
        """
        Checks if a product already exists in the database
        :param product_asin: asin number of product
        :return: bool
        """
        logger.debug('checking if product {asin} exsists in database'.format(
            asin=product_asin))
        query = QUERIES["ExistsProduct"]
        params = (product_asin,)

        try:
            success_bool = self.pg_.execute_query(self.pg_cursor, query, params)
            self.pg_.commit_changes(self.pg_conn)
            return success_bool[0][0]
        except Exception as e:
            logger.exception(e.message)
            return None

    def exists_category_in_db(self, category_id):
        """
        Checks if a category exists in database
        :param category_id: category id
        :return: bool
        """
        logger.debug('checking if category {id} exists in database'.format(
            id=category_id))
        query = QUERIES["ExistsCategory"]
        params = (category_id,)

        try:
            success_bool = self.pg_.execute_query(self.pg_cursor, query, params)
            self.pg_.commit_changes(self.pg_conn)
            return success_bool[0][0]
        except Exception as e:
            logger.exception(e.message)
            return None

    def insert_category_into_db(self, category_id):
        """
        Inserts a new category into the database
        :param category_id: id of category
        :return: bool
        """
        logger.debug('inserting new category {id} into database'.format(
            id=category_id))
        query = QUERIES["InsertCategory"]
        params = (category_id,)

        try:
            self.pg_.execute_query(self.pg_cursor, query, params)
            self.pg_.commit_changes(self.pg_conn)
            return True
        except Exception as e:
            logger.exception(e.message)
            return False

    def get_product_links_from_db(self, category_id):
        """
        Returns all product links of a category from database
        :param category_id: id of category
        :return: list of product links
        """
        logger.debug('getting product links for category {id}'.format(
            id=category_id))
        query = QUERIES["SelectProductLink"]
        params = (category_id,)

        try:
            response = self.pg_.execute_query(self.pg_cursor, query, params)
            product_links = [link[0] for link in response]
            self.pg_.commit_changes(self.pg_conn)
            return product_links
        except Exception as e:
            logger.exception(e.message)
            return None

    def get_total_reviews_from_db(self, product_asin):
        logger.debug('getting product {asin} total no of reviews from database'.format(asin=product_asin))
        query = QUERIES["GetTotalReviewCount"]
        params = (product_asin,)

        try:
            review_count = self.pg_.execute_query(self.pg_cursor, query, params)
            self.pg_.commit_changes(self.pg_conn)
            return review_count[0][0]
        except Exception as e:
            logger.exception(e.message)
            return None
