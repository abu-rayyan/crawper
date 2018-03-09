import logging

from config.config import QUERIES

logger = logging.getLogger(__name__)


# noinspection SpellCheckingInspection
class UtilityFunctions:
    def __init__(self, conn, cursor, pool):
        logger.debug('initializing utility functions')
        self.pg_pool = pool
        self.pg_conn = conn
        self.pg_cursor = cursor

    def get_product_from_db(self, product_asin):
        """
        Returns product's information from database
        :param product_asin: asin no of product
        :return: dict (product information)
        """
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

        query = QUERIES["GetProduct"]
        params = (product_asin,)

        try:
            product = self.pg_pool.execute_query(self.pg_cursor, query, params)
            self.pg_pool.commit_changes(self.pg_conn)

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
        """
        Returns a product reviews from database
        :param product_asin: asin no of product
        :return: product reviews
        """
        logger.debug('getting product {asin} reviews from database'.format(asin=product_asin))
        query = QUERIES["GetProductReviews"]
        params = (product_asin,)

        try:
            reviews = self.pg_pool.execute_query(self.pg_cursor, query, params)
            self.pg_pool.commit_changes(self.pg_conn)
            return reviews
        except Exception as e:
            logger.debug(e.message)
            return None

    def get_zero_rank_asins_from_db(self):
        """
        Return asins with ranking = 0
        :return:
        """
        logger.debug('getting all asins with zero ranks')
        query = QUERIES["GetAsinsWithZeroRank"]

        try:
            res = self.pg_pool.execute_query(self.pg_cursor, query, params='')
            self.pg_pool.commit_changes(self.pg_conn)
            return res
        except Exception as e:
            logger.exception(e.message)
            return None

    def get_products_asin_from_db(self):
        """
        Returns asin no of all products from database
        :return: asin no list
        """
        logger.debug('getting all products asin from database')
        query = QUERIES["GetProductsAsin"]

        try:
            res_data = self.pg_pool.execute_query(self.pg_cursor, query, params='')
            self.pg_pool.commit_changes(self.pg_conn)
            return res_data
        except Exception as e:
            logger.exception(e.message)
            return None

    def insert_rewiew_analysis_into_db(self, review_stat):
        """
        Inserts review's analysis data to database
        :param review_stat: analyzed review information
        :return: success bool
        """
        logger.debug('inserting review analysis into database')
        query = QUERIES["InsertReviewStat"]
        params = (review_stat["ReviewLink"], review_stat["ReviewLength"],
                  review_stat["WordCountCategory"], review_stat["SentimentScore"],
                  review_stat["SentimentLabel"], review_stat["CommonPhrase"],
                  review_stat["CredulityScore"], review_stat["ReviewScore"])

        try:
            self.pg_pool.execute_query(self.pg_cursor, query, params)
            self.pg_pool.commit_changes(self.pg_conn)
            return True
        except Exception as e:
            logger.exception(e.message)
            return False

    def get_reviewers_ids_from_db(self):
        """
        Returns all reviewer's ids from database
        :return: reviewer ids list
        """
        logger.debug('getting reviewers information from database')
        query = QUERIES["GetReviewerIds"]
        params = [116400]
        try:
            reviewer_ids = self.pg_pool.execute_query(self.pg_cursor, query, params)
            self.pg_pool.commit_changes(self.pg_conn)
            return reviewer_ids
        except Exception as e:
            logger.exception(e.message)
            return None

    def get_reviewers_total_reviews_from_db(self, reviewer_id):
        """
        Returns total reviewer of a reviewer from database
        :param reviewer_id: id of reviewer
        :return: total reviews
        """
        logger.debug('getting reviewer {id} total no of reviews  and ratings from database'.format(id=reviewer_id))
        query = QUERIES["GetTotalReviewsOfReviewer"]
        params = (reviewer_id,)

        try:
            reviews_rate = self.pg_pool.execute_query(self.pg_cursor, query, params)
            self.pg_pool.commit_changes(self.pg_conn)
            return reviews_rate
        except Exception as e:
            logger.exception(e.message)
            return None

    def update_reviewer_creduality_in_db(self, reviewer_data):
        """
        Updates reviewer's creduality and participation history to database
        :param reviewer_data: reviewer data dictionary
        :return: success bool
        """
        logger.debug('updating reviewer {id} creduality score'.format(id=reviewer_data["ReviewerId"]))
        query = QUERIES["UpdateReviewerCredualityScore"]
        params = (
            reviewer_data["TotalReviews"], reviewer_data["CredualityScore"], reviewer_data["ParticipationHistory"],
            reviewer_data["ReviewerId"])

        try:
            self.pg_pool.execute_query(self.pg_cursor, query, params)
            self.pg_pool.commit_changes(self.pg_conn)
            return True
        except Exception as e:
            logger.exception(e.message)
            return False

    def get_product_reviews_text_from_db(self, asin):
        """
        Returns a product reviews texts from database
        :param asin: asin no of product
        :return: review text list
        """
        logger.debug('getting product {asin} all reviews text from database'.format(asin=asin))
        query = QUERIES["GetProductReviewsText"]
        params = (asin,)

        try:
            reviews_text = self.pg_pool.execute_query(self.pg_cursor, query, params)
            self.pg_pool.commit_changes(self.pg_conn)
            return reviews_text
        except Exception as e:
            logger.exception(e.message)
            return None

    def get_reviewer_creduality_from_db(self, reviewer_id):
        """
        Returns reviewer's creduality score from database
        :param reviewer_id: reviewer id
        :return: creduality score
        """
        logger.debug('getting reviewer {id} creaduality from database'.format(id=reviewer_id))
        query = QUERIES["GetReviewerCreaduality"]
        params = (reviewer_id,)

        try:
            creduality = self.pg_pool.execute_query(self.pg_cursor, query, params)
            self.pg_pool.commit_changes(self.pg_conn)
            return creduality
        except Exception as e:
            logger.exception(e.message)
            return None

    @staticmethod
    def calculate_participation_history(no_of_reviews):
        """
        Calculates and returns reviewers participation history label
        :param no_of_reviews: no of total reviewes of reviewer
        :return: participation history label
        """
        logger.debug('calculating reviewer participation hisotry')
        try:
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
        except Exception as e:
            logger.exception(e.message)
            return None

    def get_reviewers_from_db(self, product_asin):
        """
        Returns product reviewers from database
        :param product_asin: asin no of product
        :return: product reviewer's information
        """
        logger.debug('getting reviewrs info of product {product}'.format(product=product_asin))
        query = QUERIES["GetProductReviewers"]
        params = (product_asin,)

        try:
            product_reviewers_info = self.pg_pool.execute_query(self.pg_cursor, query, params)
            self.pg_pool.commit_changes(self.pg_conn)
            return product_reviewers_info
        except Exception as e:
            logger.exception(e.message)
            return None

    def get_all_reviewers_from_db(self, product_asin):
        """
        Returns all reviewers from database
        :param product_asin: asin no of product
        :return: reviewers list
        """
        logger.debug('getting reviewers of all products from db')
        try:
            products_asin = self.get_products_asin_from_db()
            all_product_reviews = []
            for asin in products_asin:
                if not asin == product_asin:
                    product_reviews = self.get_reviewers_from_db(asin[0])
                    all_product_reviews.append(product_reviews)
            return all_product_reviews
        except Exception as e:
            logger.exception(e.message)
            return None

    def get_product_reviews_with_four_five_stars(self, product_asin):
        """
        Returns product reviews having rate greater than or equal to 4.0
        :param product_asin: asin no of product
        :return: reviews list
        """
        logger.debug('getting 4-5 star reviews of product {asin} from database'.format(asin=product_asin))
        query = QUERIES["Get45StarProductReviews"]
        params = (product_asin,)

        try:
            reviews_text = self.pg_pool.execute_query(self.pg_cursor, query, params)
            self.pg_pool.commit_changes(self.pg_conn)
            return reviews_text
        except Exception as e:
            logger.exception(e.message)
            return None

    def get_reviewers_with_one_review_from_db(self):
        """
        Returns all reviewer ids with only one review from database
        :return: reviewer ids list
        """
        logger.debug('getting reviewers with one review from database')
        query = QUERIES["GetReviewersWithOneReview"]

        try:
            reviewer_ids = self.pg_pool.execute_query(self.pg_cursor, query, params='')
            self.pg_pool.commit_changes(self.pg_conn)
            return reviewer_ids
        except Exception as e:
            logger.exception(e.message)
            return None

    def get_all_reviewers_with_four_five_stars(self):
        """
        Returns all reviewer ids with review rate >= 4.0
        :return: reviewer ids list
        """
        logger.debug('getting reviewers of 4-5 star reviews from database')
        query = QUERIES["Get45StarReviewers"]

        try:
            reviewer_ids = self.pg_pool.execute_query(self.pg_cursor, query, params='')
            self.pg_pool.commit_changes(self.pg_conn)
            return reviewer_ids
        except Exception as e:
            logger.exception(e.message)
            return None

    def get_reviewer_reviewes_date_from_db(self, reviewer_id):
        """
        Returns all dates of reviewer's reviews from database
        :param reviewer_id: reviewer id
        :return: dates list
        """
        logger.debug('getting reviews date of reviewer {id}'.format(id=reviewer_id))
        query = QUERIES["GetReviewerReviewsDate"]
        params = (reviewer_id,)

        try:
            reviews_dates = self.pg_pool.execute_query(self.pg_cursor, query, params)
            self.pg_pool.commit_changes(self.pg_conn)
            return reviews_dates
        except Exception as e:
            logger.exception(e.message)
            return None

    @staticmethod
    def get_no_duplicates(item_list):
        """
        Returns total no of duplicates from a list of items
        :param item_list: items list
        :return: total no of duplicates
        """
        try:
            new_list = []
            no_duplicates = 0
            for item in item_list:
                if item not in new_list:
                    new_list.append(item)
                else:
                    no_duplicates += 1
            return no_duplicates
        except Exception as e:
            logger.exception(e.message)
            return None

    def get_total_no_of_reviewes_of_reviewer_from_db(self, reviewer_id):
        """
        Returns total no of reviews of reviewer from database
        :param reviewer_id: reviewer id
        :return: total no of reviews
        """
        logger.debug('getting total no of reviewes of reviewer {id} from database'.format(id=reviewer_id))
        query = QUERIES["GetTotalNoReviewesOfReviewer"]
        params = (reviewer_id,)

        try:
            total_reviews = self.pg_pool.execute_query(self.pg_cursor, query, params)
            self.pg_pool.commit_changes(self.pg_conn)
            return total_reviews
        except Exception as e:
            logger.exception(e.message)
            return None

    def get_four_five_star_reviews_of_reviewer_from_db(self, reviewer_id):
        """
        Returns reviews of reviewer from database having rate >= 4.0
        :param reviewer_id: reviewer id
        :return: reviews list
        """
        logger.debug('getting 4-5 star reviews of reviewer {id} from database'.format(id=reviewer_id))
        query = QUERIES["GetReviewer45StarReviews"]
        params = (reviewer_id,)

        try:
            reviews = self.pg_pool.execute_query(self.pg_cursor, query, params)
            self.pg_pool.commit_changes(self.pg_conn)
            return reviews
        except Exception as e:
            logger.exception(e.message)
            return None

    def get_review_rate_of_reviews_of_product(self, product_asin):
        """
        Returns all rates of reviews of product
        :param product_asin: asin no of product
        :return: rates list
        """
        logger.debug('getting review rates of reviews of product {asin}'.format(asin=product_asin))
        query = QUERIES["GetRatesOfReviewsOfProduct"]
        params = (product_asin,)

        try:
            review_rates = self.pg_pool.execute_query(self.pg_cursor, query, params)
            self.pg_pool.commit_changes(self.pg_conn)
            return review_rates
        except Exception as e:
            logger.exception(e.message)
            return None

    def get_total_no_three_star_reviews_of_product_from_db(self, product_asin):
        """
        Returns total number of three star reviews of product from database
        :param product_asin: asin no of product
        :return: total no of reviews
        """
        logger.debug("getting total no of 3 star reviews of product {asin}".format(asin=product_asin.decode('utf-8')))
        query = QUERIES["GetNoOf3StarReviewsOfProduct"]
        params = (product_asin,)

        try:
            total_reviews = self.pg_pool.execute_query(self.pg_cursor, query, params)
            self.pg_pool.commit_changes(self.pg_conn)
            return total_reviews
        except Exception as e:
            logger.exception(e.message)
            return None

    def get_total_no_one_two_star_reviews_of_product_from_db(self, product_asin):
        """
        Returns total no of 1-2 star reviews of a product from database
        :param product_asin: asin no of product
        :return: total no of reviews
        """
        logger.debug("getting total no of 1-2 star reviews of product {asin}".format(asin=product_asin))
        query = QUERIES["GetNoOf1to2StarReviewsOfProduct"]
        params = (product_asin,)

        try:
            total_reviews = self.pg_pool.execute_query(self.pg_cursor, query, params)
            self.pg_pool.commit_changes(self.pg_conn)
            return total_reviews
        except Exception as e:
            logger.exception(e.message)
            return None

    def get_reviews_reviewer_ids_from_db(self, product_asin):
        """
        Returns reviewer ids of a product reviews from database
        :param product_asin: asin no of product
        :return: reviewer ids list
        """
        logger.debug('getting reviewer ids of product {asin} reviews from database'.format(
            asin=product_asin.decode('utf-8')))
        query = QUERIES["GetReviewerIdsOfProductReviews"]
        params = (product_asin,)

        try:
            reviewer_ids = self.pg_pool.execute_query(self.pg_cursor, query, params)
            self.pg_pool.commit_changes(self.pg_conn)
            return reviewer_ids
        except Exception as e:
            logger.exception(e.message)
            return None

    def get_reviewers_participation_from_db(self, reviewer_id):
        """
        Returns a reviewer's participation history from database
        :param reviewer_id: reviewer id
        :return: participation history label
        """
        logger.debug('getting reviewer {reviewer_id} participation history from db'.format(reviewer_id=reviewer_id))
        query = QUERIES["GetReviewerParticipationHistory"]
        params = (reviewer_id,)

        try:
            participt_history = self.pg_pool.execute_query(self.pg_cursor, query, params)
            self.pg_pool.commit_changes(self.pg_conn)
            return participt_history
        except Exception as e:
            logger.exception(e.message)
            return None

    def get_product_reviews_dates_from_db(self, product_asin):
        """
        Returns product's reviews dates from database
        :param product_asin: asin no of product
        :return: dates list
        """
        logger.debug('getting product {asin} reviews dates from database'.format(asin=product_asin.decode('utf-8')))
        query = QUERIES["GetProductReviewsDates"]
        params = (product_asin,)

        try:
            reviews_dates = self.pg_pool.execute_query(self.pg_cursor, query, params)
            self.pg_pool.commit_changes(self.pg_conn)
            return reviews_dates
        except Exception as e:
            logger.exception(e.message)
            return None

    def get_product_today_reviews_from_db(self, product_asin, t_date):
        """
        Get present day reviews of product from database
        :param product_asin: asin no of product
        :param t_date: present date
        :return: total no of reviews
        """
        logger.debug('getting today reviews of product {asin} from database'.format(asin=product_asin))
        query = QUERIES["GetNoOfTodayReviewsOfProduct"]
        params = (product_asin, t_date,)

        try:
            total_reviews = self.pg_pool.execute_query(self.pg_cursor, query, params)
            self.pg_pool.commit_changes(self.pg_conn)
            return total_reviews
        except Exception as e:
            logger.exception(e.message)
            return None

    def get_review_ids_of_reviewer_from_db(self, reviewer_id):
        """
        Returns review ids of reviewer from database
        :param reviewer_id: reviewer id
        :return: reviewer ids
        """
        logger.debug('getting reviews ids of reviewer {id} from database'.format(id=reviewer_id))
        query = QUERIES["GetReviewsIdsOfReviewer"]
        params = (reviewer_id,)

        try:
            review_ids = self.pg_pool.execute_query(self.pg_cursor, query, params)
            self.pg_pool.commit_changes(self.pg_conn)
            return review_ids
        except Exception as e:
            logger.exception(e.message)
            return None

    def get_review_score_from_db(self, review_id):
        """
        Returns a review's score from database
        :param review_id: review link or id
        :return: review score
        """
        logger.debug('getting review {id} score from database'.format(id=review_id))
        query = QUERIES["GetReviewScore"]
        params = (review_id,)

        try:
            review_score = self.pg_pool.execute_query(self.pg_cursor, query, params)
            self.pg_pool.commit_changes(self.pg_conn)
            return review_score
        except Exception as e:
            logger.exception(e.message)
            return None

    def update_review_score_in_db(self, review_id, score):
        """
        Updates review score in database
        :param review_id: review link or id
        :param score: updated score
        :return: success bool
        """
        logger.debug('updating review {id} score in database'.format(id=review_id))
        query = QUERIES["UpdateReviewScore"]
        params = (score, review_id,)

        try:
            self.pg_pool.execute_query(self.pg_cursor, query, params)
            self.pg_pool.commit_changes(self.pg_conn)
            return True
        except Exception as e:
            logger.exception(e.message)
            return False

    def get_product_rank_from_db(self, product_asin):
        """
        Returns product score from database
        :param product_asin:
        :return:
        """
        logger.debug('getting product {id} rank from database'.format(id=product_asin))
        query = QUERIES["GetProductRank"]
        params = (product_asin,)

        try:
            product_score = self.pg_pool.execute_query(self.pg_cursor, query, params)
            self.pg_pool.commit_changes(self.pg_conn)
            return product_score
        except Exception as e:
            logger.exception(e.message)
            return None

    def update_product_rank_in_db(self, product_asin, score):
        """
        Updates product rank in database
        :param product_asin: asin no of product
        :param score: ranking score
        :return: success bool
        """
        logger.debug('updating product {asin} rank in database'.format(asin=product_asin))
        query = QUERIES["UpdateProductRank"]
        params = (score, product_asin,)

        try:
            self.pg_pool.execute_query(self.pg_cursor, query, params)
            self.pg_pool.commit_changes(self.pg_conn)
            return True
        except Exception as e:
            logger.exception(e.message)
            return False

    def get_review_text_from_db(self, review_id):
        """
        Get review text from database
        :param review_id: review id or link
        :return: review text
        """
        logger.debug('getting review {link} text from database'.format(link=review_id.decode('utf-8')))
        query = QUERIES["GetReviewText"]
        params = (review_id,)

        try:
            review_text = self.pg_pool.execute_query(self.pg_cursor, query, params)
            self.pg_pool.commit_changes(self.pg_conn)
            return review_text
        except Exception as e:
            logger.exception(e.message)
            return None
