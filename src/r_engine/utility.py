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
        params = (
            reviewer_data["TotalReviews"], reviewer_data["CredualityScore"], reviewer_data["ParticipationHistory"],
            reviewer_data["ReviewerId"])

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

    @staticmethod
    def calculate_participation_history(no_of_reviews):
        logger.debug('calculating reviewer participation hisotry')
        if 0 <= no_of_reviews <= 1:
            return 'R1'
        elif 2 <= no_of_reviews <= 5:
            return 'R2'
        elif 6 <= no_of_reviews <= 10:
            return 'R3'
        elif 11 <= no_of_reviews <= 20:
            return 'R4'
        elif 21 <= no_of_reviews <= 30:
            return 'R5'
        elif 31 <= no_of_reviews <= 40:
            return 'R6'
        elif 41 <= no_of_reviews <= 50:
            return 'R7'
        elif 51 <= no_of_reviews <= 60:
            return 'R8'
        else:
            return 'R9'

    def get_reviewers_from_db(self, product_asin):
        logger.debug('getting reviewrs info of product {product}'.format(product=product_asin))
        pg_conn, pg_cursor = self.pg_pool.get_conn()
        query = QUERIES["GetProductReviewers"]
        params = (product_asin,)

        try:
            product_reviewers_info = self.pg_pool.execute_query(pg_cursor, query, params)
            self.pg_pool.commit_changes(pg_conn)
            self.pg_pool.put_conn(pg_conn)
            return product_reviewers_info
        except Exception as e:
            logger.exception(e.message)
            self.pg_pool.put_conn(pg_conn)
            return None

    def get_all_reviewers_from_db(self, product_asin):
        logger.debug('getting reviewers of all products from db')
        products_asin = self.get_products_asin_from_db()
        all_product_reviews = []
        for asin in products_asin:
            if not asin == product_asin:
                product_reviews = self.get_reviewers_from_db(asin[0])
                all_product_reviews.append(product_reviews)
        return all_product_reviews

    def get_product_reviews_with_four_five_stars(self, product_asin):
        logger.debug('getting 4-5 star reviews of product {asin} from database'.format(asin=product_asin))
        pg_conn, pg_cursor = self.pg_pool.get_conn()
        query = QUERIES["Get45StarProductReviews"]
        params = (product_asin,)

        try:
            reviews_text = self.pg_pool.execute_query(pg_cursor, query, params)
            self.pg_pool.commit_changes(pg_conn)
            self.pg_pool.put_conn(pg_conn)
            return reviews_text
        except Exception as e:
            logger.exception(e.message)
            self.pg_pool.put_conn(pg_conn)
            return None

    def get_reviewers_with_one_review_from_db(self):
        logger.debug('getting reviewers with one review from database')
        pg_conn, pg_cursor = self.pg_pool.get_conn()
        query = QUERIES["GetReviewersWithOneReview"]

        try:
            reviewer_ids = self.pg_pool.execute_query(pg_cursor, query, params='')
            self.pg_pool.commit_changes(pg_conn)
            self.pg_pool.put_conn(pg_conn)
            return reviewer_ids
        except Exception as e:
            logger.exception(e.message)
            self.pg_pool.put_conn(pg_conn)
            return None

    def get_all_reviewers_with_four_five_stars(self):
        logger.debug('getting reviewers of 4-5 star reviews from database')
        pg_conn, pg_cursor = self.pg_pool.get_conn()
        query = QUERIES["Get45StarReviewers"]

        try:
            reviewer_ids = self.pg_pool.execute_query(pg_cursor, query, params='')
            self.pg_pool.commit_changes(pg_conn)
            self.pg_pool.put_conn(pg_conn)
            return reviewer_ids
        except Exception as e:
            logger.exception(e.message)
            self.pg_pool.put_conn(pg_conn)
            return None

    def get_reviewer_reviewes_date_from_db(self, reviewer_id):
        logger.debug('getting reviews date of reviewer {id}'.format(id=reviewer_id))
        pg_conn, pg_cursor = self.pg_pool.get_conn()
        query = QUERIES["GetReviewerReviewsDate"]
        params = (reviewer_id,)

        try:
            reviews_dates = self.pg_pool.execute_query(pg_cursor, query, params)
            self.pg_pool.commit_changes(pg_conn)
            self.pg_pool.put_conn(pg_conn)
            return reviews_dates
        except Exception as e:
            logger.exception(e.message)
            self.pg_pool.put_conn(pg_conn)
            return None

    @staticmethod
    def get_no_duplicates(item_list):
        new_list = []
        no_duplicates = 0
        for item in item_list:
            if item not in new_list:
                new_list.append(item)
            else:
                no_duplicates += 1
        return no_duplicates

    def get_total_no_of_reviewes_of_reviewer_from_db(self, reviewer_id):
        logger.debug('getting total no of reviewes of reviewer {id} from database'.format(id=reviewer_id))
        pg_conn, pg_cursor = self.pg_pool.get_conn()
        query = QUERIES["GetTotalNoReviewesOfReviewer"]
        params = (reviewer_id,)

        try:
            total_reviews = self.pg_pool.execute_query(pg_cursor, query, params)
            self.pg_pool.commit_changes(pg_conn)
            self.pg_pool.put_conn(pg_conn)
            return total_reviews
        except Exception as e:
            logger.exception(e.message)
            self.pg_pool.put_conn(pg_conn)
            return None

    def get_four_five_star_reviews_of_reviewer_from_db(self, reviewer_id):
        logger.debug('getting 4-5 star reviews of reviewer {id} from database'.format(id=reviewer_id))
        pg_conn, pg_cursor = self.pg_pool.get_conn()
        query = QUERIES["GetReviewer45StarReviews"]
        params = (reviewer_id,)

        try:
            reviews = self.pg_pool.execute_query(pg_cursor, query, params)
            self.pg_pool.commit_changes(pg_conn)
            self.pg_pool.put_conn(pg_conn)
            return reviews
        except Exception as e:
            logger.exception(e.message)
            self.pg_pool.put_conn(pg_conn)
            return None

    def get_review_rate_of_reviews_of_product(self, product_asin):
        logger.debug('getting review rates of reviews of product {asin}'.format(asin=product_asin))
        pg_conn, pg_cursor = self.pg_pool.get_conn()
        query = QUERIES["GetRatesOfReviewsOfProduct"]
        params = (product_asin,)

        try:
            review_rates = self.pg_pool.execute_query(pg_cursor, query, params)
            self.pg_pool.commit_changes(pg_conn)
            self.pg_pool.put_conn(pg_conn)
            return review_rates
        except Exception as e:
            logger.exception(e.message)
            self.pg_pool.put_conn(pg_conn)
            return None
