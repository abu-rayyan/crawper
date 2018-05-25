from __future__ import print_function
import logging
import nltk
import math

from nltk.util import ngrams
from utility import UtilityFunctions
from textblob import TextBlob
from triggers import Triggers
from src.common.db.postgres_pool import PgPool

logger = logging.getLogger(__name__)


# noinspection SpellCheckingInspection
class REngine:
    def __init__(self):
        logger.debug('initiating AEngine')
        self.pg_pool = PgPool()
        self.pg_conn, self.pg_cursor = self.pg_pool.get_conn()
        self.utility_method = UtilityFunctions(self.pg_conn, self.pg_cursor, self.pg_pool)
        self.triggers = Triggers(self.pg_conn, self.pg_cursor, self.pg_pool)

    def put_db_connection_back(self):
        """
        Puts db connections back to pool
        """
        logger.debug('putting database connection object back in pool')
        self.pg_pool.commit_changes(self.pg_conn)
        self.pg_pool.put_conn(self.pg_conn)

    def start_engine(self):
        """
        Starts the REngine to start the data analytics
        """
        logger.info('starting analysis engine')
        #self.calculate_reviewer_creduality()
        self.analyze_products()

    def analyze_products(self):
        """
        Calls all product analysis functionality of REngine
        """
        logger.info('analyzing products information')
        asins = self.utility_method.get_products_asin_from_db()
        if asins is not None:
            for asin in asins:
                try:
                    self.calculate_reviewer_creduality(asin[0])
                    #self.analyze_product(asin[0])
                    #self.generate_product_triggers(asin[0])
                except Exception as e:
                    logger.exception(e.message)
        else:
            logger.error('something bad happened')

    def calculate_reviewer_creduality(self, product_asin):
        """
        Calculates reviewer's credulity's and Participation histories
        """
        logger.debug('calculating reviewer creduality')
        try:
            print (product_asin)
            reviewer_ids = self.utility_method.get_reviewers_ids_from_reviews(product_asin)
            reviewer_data = {
                "ReviewerId": None,
                "TotalReviews": None,
                "CredualityScore": None,
                "ParticipationHistory": None,
                "one_off_trigger": None,
                "multiple_single_day_trigger": None
            }

            if reviewer_ids:
                for reviewer_id in reviewer_ids:
                    print (reviewer_id)
                    reviewer_data["ReviewerId"] = reviewer_id[0]
                    reviews = self.utility_method.get_reviewers_total_reviews_from_db(reviewer_id[0])
                    reviewer_data["TotalReviews"] = len(reviews)
                    rates = [rate[0] for rate in reviews]

                    sum_rates = 0
                    for rate in rates:
                        sum_rates += float(rate)

                    reviewer_data["CredualityScore"] = sum_rates / float(len(reviews)) if \
                        reviewer_data["TotalReviews"] else 0
                    reviewer_data["ParticipationHistory"] = self.utility_method.calculate_participation_history(
                        reviewer_data["TotalReviews"])
                    # handling one_off_review_trigger
                    if len(reviews) == 1:
                        print("trigger on")
                        trigger = '1'
                    else:
                        trigger = '0'

                    reviewer_data["one_off_trigger"] = trigger

                    reviewer_data["multiple_single_day_trigger"] = \
                        self.triggers.get_multiple_single_day_reviews_trigger(reviewer_data["ReviewerId"])
                    if self.utility_method.update_reviewer_creduality_in_db(reviewer_data):
                        logger.debug('total reviews & creduality update success')
                    else:
                        logger.debug('error in updating creduality & total reviews')
                self.analyze_product(product_asin)
                self.generate_product_triggers(product_asin)
                self.utility_method.update_status_reviews(product_asin, trigger=True)
                print ("********* Trigger On ***********")
            else:
                logger.debug('error in fetching reviewer ids from database')
        except Exception as e:
            logger.exception(e.message)

    def analyze_product(self, asin):
        """
        Analyze and perform analytics on a single product's data
        :param asin: asin no of the product
        """
        try:
            logger.debug('analyzing product {asin}'.format(asin=asin))
            logger.debug('getting product reviews from database')
            product_reviews = self.utility_method.get_product_reviews_from_db(asin)
            if product_reviews is not None:
                self.analyze_reviews(product_reviews, asin)
            else:
                logger.error('unknown error, product reviews is None')
        except Exception as e:
            logger.exception(e.message)

    def analyze_reviews(self, reviews, asin):
        """
        Analyzes all reviews of a product
        :param reviews: list of a product's reviews
        :param asin: asin no of the product
        """
        logger.debug('analyzing reviews {review}'.format(review=reviews))

        #reviews_text = self.utility_method.get_product_reviews_text_from_db(asin)
        reviews_commons = []
        '''
        try:
            if reviews_text:
                reviews_commons = self.find_common_phrases_in_reviews(reviews_text)
        except Exception as e:
            logger.exception(e.message)
        '''

        try:
            avg_length = self.avg_word_len_category(asin)

            for review in reviews:
                trigger_list = []
                review_stats = {
                    "ReviewLink": review[0],
                    "ReviewLength": None,
                    "WordCountCategory": None,
                    "SentimentScore": None,
                    "SentimentLabel": None,
                    "CommonPhrase": None,
                    "CredulityScore": None,
                    "ReviewScore": None,
                    "AvgWordLengthTrigger": None
                }
                if not self.utility_method.exists_review_link(review[0]):
                    try:
                        blob = TextBlob(review[3].decode('utf-8'))
                        review_stats["ReviewLength"] = len(blob.words)
                        logger.debug('ReviewLength: {length}'.format(length=review_stats["ReviewLength"]))
                        review_stats["SentimentScore"] = blob.sentiment.polarity * 100  # score between -100 to +100
                        review_stats["SentimentLabel"] = self.get_sentiment_label(review_stats["SentimentScore"])
                        # return credulity score, one_off_review multiple_single_day_trigger, total_reviews
                        credulity_and_triggers = self.utility_method.get_reviewer_creduality_from_db(review[5])
                        review_stats["CredulityScore"] = credulity_and_triggers[0][0]
                        review_stats["WordCountCategory"] = self.get_word_count_category(avg_length["AvgWordLength"],
                                                                                         review_stats["ReviewLength"])
                        # review_stats["CommonPhrase"] = self.is_most_common_phrase_exists(review[3].decode('utf-8'),reviews_commons)
                        review_stats["AvgWordLengthTrigger"] = self.word_volume_trigger(asin, review_stats["ReviewLength"])

                        scaling_factor = 50
                        temporary_score = scaling_factor*(review[4]) + review_stats["SentimentScore"] + (1/(review_stats["CredulityScore"]*scaling_factor))

                        # triggers helps in calculation of review score
                        if credulity_and_triggers[0][1]:
                            trigger_list.append(1)
                        if credulity_and_triggers[0][2]:
                            trigger_list.append(1)
                        if review_stats["AvgWordLengthTrigger"] == '1':
                            trigger_list.append(1)
                        total_reviews = credulity_and_triggers[0][3]
                        status = self.generate_reviewer_reliability_status(review[5], total_reviews, trigger_list)
                        review_stats["ReviewScore"] = self.get_review_score(temporary_score, status)
                        print (review_stats["ReviewScore"])
                        print(review_stats["ReviewLink"])
                    except Exception as e:
                        logger.exception(e.message)
                    self.utility_method.insert_rewiew_analysis_into_db(review_stats)
                    print ("inserted into review analysis")

        except Exception as e:
            logger.exception(e.message)

    @staticmethod
    def get_sentiment_label(sentiment_score):
        """
        Returns sentiment label for a sentiment score
        :param sentiment_score: sentiment score of text
        :return: sentiment label
        """
        logger.debug('generating sentiment label')

        try:
            if -100 <= sentiment_score < -50:
                return 'angry'
            elif -50 <= sentiment_score < -10:
                return 'dissatisfied'
            elif -10 <= sentiment_score < 10:
                return 'neutral'
            elif 10 <= sentiment_score < 50:
                return 'satisfied'
            elif 50 <= sentiment_score <= 100:
                return 'happy'
            else:
                return None
        except Exception as e:
            logger.exception(e.message)
            return None

    @staticmethod
    def get_word_count_category(avg_review_length, review_length):
        """
        Returns Word-Count-Category of a review
        :param avg_review_length: average review length of a product
        :param review_length: length of the target review
        :return: Word Count Category
        """
        logger.debug('generating word count category')
        try:
            if 0 * avg_review_length <= review_length <= 0.25 * avg_review_length:
                return "A"
            elif 0.25 * avg_review_length <= review_length <= 2 * review_length:
                return "B"
            elif 2 * avg_review_length <= review_length:
                return "C"
            else:
                return "Error"
        except Exception as e:
            logger.exception(e.message)
            return "Error"

    @staticmethod
    def find_common_phrases_in_reviews(reviews):
        """
        Finds and returns most config phrases in reviews of a product
        :param reviews: list of reviews
        :return: list of most config phrases
        """
        logger.debug('finding config phrases in reviews {reviews}'.format(reviews=reviews))
        try:
            combined_review_text = ''
            most_common_phrases = []
            for review in reviews:
                combined_review_text += ' ' + review[0].decode('utf-8')

            trigrams = ngrams(combined_review_text.split(), 3)
            freq = nltk.FreqDist(trigrams)
            decision_freq = math.ceil(freq.most_common(1)[0][1] * 0.2)  # round off to nearest integer
            most_common = freq.most_common()
            for key, val in most_common:
                if val > decision_freq:
                    most_common_phrases.append(key)

            return most_common_phrases
        except Exception as e:
            logger.exception(e.message)
            return None

    @staticmethod
    def is_most_common_phrase_exists(review, reviews_commons):
        """
        Checks if a most config phrase exists in target review
        :param review: target review
        :param reviews_commons: list of config phrases in reviews
        :return: bool (True/False)
        """
        logger.debug('checking if most config phrase also found in most config phrases of reviews')

        try:
            trigrams = ngrams(review.split(), 3)
            freq = nltk.FreqDist(trigrams)
            most_common = freq.most_common(1)

            if not len(most_common) == 0:
                match_count = 0
                for key, val in most_common:
                    if key in reviews_commons:
                        match_count += 1
                    else:
                        continue
                if match_count > 0:
                    return True
                else:
                    return False
            else:
                return False

        except Exception as e:
            logger.exception(e.message)
            return None

    @staticmethod
    def get_no_of_reviews_having_most_common(reviews):
        """
        Returns no of reviews which have most config phrase in them
        :param reviews: list of reviews
        :return: no of reviews & percentage reviews having most config phrase
        """
        logger.debug('finding config phrases in reviews {reviews}'.format(reviews=reviews))
        try:
            combined_review_text = ''
            for review in reviews:
                combined_review_text += ' ' + review[0].decode('utf-8')

            trigrams = ngrams(combined_review_text.split(), 3)
            freq = nltk.FreqDist(trigrams)
            most_common = freq.most_common(1)

            match_count = 0
            if not most_common == 0:
                for review in reviews:
                    review_text = review[0].decode('utf-8')
                    tri_grams = ngrams(review_text.split(), 3)
                    for key, val in most_common:
                        if key in tri_grams:
                            match_count += 1
                        else:
                            continue
            percent_reviews = (float(match_count) / float(len(reviews))) * 100
            return match_count, percent_reviews
        except Exception as e:
            logger.exception(e.message)
            return None

    def generate_reviewer_reliability_status(self, reviewer_id, total_reviews, trigger_list):
        """
        Returns a reviewer's reliability status based on trigger list
        :param reviewer_id: id of reviewer
        :param trigger_list: activated triggers list
        :return: reliability status of reviewer
        """
        logger.debug('generating reviewer {reviewer_id} reliability status'.format(reviewer_id=reviewer_id))
        try:
            duplicated_reviews_trigger = self.triggers.get_duplicated_reviews_trigger(reviewer_id, total_reviews)

            if duplicated_reviews_trigger:
                trigger_list.append(1)

            total_triggers = len(trigger_list)
            if total_triggers >= 3:
                return 'RED'
            elif total_triggers == 2:
                return 'YELLOW'
            elif total_triggers < 2:
                return 'GREEN'
        except Exception as e:
            logger.exception(e.message)
            return None

    @staticmethod
    def get_review_score(score, reviewer_status):
        """
        Calculates and returns a review score
        :param score: previous score of review
        :param reviewer_status: reliability status of reviewer
        :return: updated review score
        """
        logger.debug('calculating review score')
        try:
            if reviewer_status == 'GREEN':
                return score + 60
            elif reviewer_status == 'YELLOW':
                return score + 30
            elif reviewer_status == 'RED':
                return score - 60
        except Exception as e:
            logger.exception(e.message)
            return None

    def get_repeated_remarks_trigger(self, review_id, product_asin):
        """
        Get repeated remarks trigger for a review and product
        :param review_id: review id or link
        :param product_asin: asin no of product being reviewed
        :return: success bool
        """
        logger.debug('generating repeated remarks trigger')

        try:
            product_reviews = self.utility_method.get_product_reviews_text_from_db(product_asin)
            review_text = self.utility_method.get_review_text_from_db(review_id)[0][0]
            review_common = self.find_common_phrases_in_reviews(product_reviews)
            return self.is_most_common_phrase_exists(review_text, review_common)
        except Exception as e:
            logger.exception(e.message)
            return False

    def avg_word_len_category(self, product_asin):

        # Getting Category from products table
        category = self.utility_method.get_distinct_category_from_products(product_asin)
        product_asin = self.utility_method.get_product_asin_from_products(category[0][0])
        no_of_products = len(product_asin)
        print(self.utility_method.check_category_in_avg_word_len(category[0][0]))
        # checking if category exists in average word volume table
        avg_length = self.calculate_word_length(product_asin, no_of_products, category[0])
        if not self.utility_method.check_category_in_avg_word_len(category[0][0]):
            self.utility_method.insert_in_avg_word_len(avg_length)
        elif self.utility_method.check_category_in_avg_word_len(category[0][0])[0][0] != no_of_products:
            self.utility_method.update_in_avg_word_len(avg_length)
        else:
            print(" category is present and new products not come yet ")
        return avg_length

    def calculate_word_length(self, product_asin, no_of_products, category):
        avg_length = {
            "CategoryName": None,
            "AvgWordLength": None,
            "NoOfProducts": None
        }
        reviews_length = []
        for pa in product_asin:
            reviews = self.utility_method.get_product_reviews(pa[0])
            for review in reviews:
                blob = TextBlob(review[0].decode('utf-8'))
                reviews_length.append(len(blob.words))

        avg_length["AvgWordLength"] = sum(reviews_length) / len(reviews_length)
        avg_length["NoOfProducts"] = no_of_products
        avg_length["CategoryName"] = category[0]
        print(avg_length)
        return avg_length

    def word_volume_trigger(self, product_asin, avg_word_length):
        category = self.utility_method.get_category_using_productasin(product_asin)[0][0]
        print (category)
        avg_review_length_category = self.utility_method.get_avg_word_length(category)[0][0]
        if avg_review_length_category and avg_word_length:
            if int(avg_word_length) < 0.2 * avg_review_length_category or int(avg_word_length) > 2.5 * avg_review_length_category:
                trigger = '1'
                return trigger
            else:
                trigger = '0'
                return trigger
        return False

    def generate_product_triggers(self, product_asin):
        """
        Checks and generates all the triggers for product, reviews and reviewers
        :param product_asin: asin no of product
        """
        logger.debug('checking and generating triggers for product {asin}'.format(asin=product_asin))
        trigger_list = []
        try:
            abnormal_review_trigger = self.triggers.get_abnormal_review_trigger(product_asin)
            if abnormal_review_trigger:
                trigger_list.append(1)
            total_reviews = self.utility_method.get_product_reviews(product_asin)
            product_trigger = len(total_reviews)*(-5)*len(trigger_list)
            try:
                reviews_score = 0
                product_score = self.utility_method.get_product_rank_from_db(product_asin)[0][0]
                product_reviews = self.utility_method.get_product_reviews_from_db(product_asin)
                for review in product_reviews:
                    try:
                        score = self.utility_method.get_review_score_from_db(review[0])[0][0]
                        reviews_score += score
                    except Exception as e:
                        logger.exception(e.message)
                product_score += reviews_score + product_trigger
                self.utility_method.update_product_rank_in_db(product_asin, product_score)
            except Exception as e:
                logger.exception(e.message)
        except Exception as e:
            logger.exception(e.message)