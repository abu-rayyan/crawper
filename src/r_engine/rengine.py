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
        self.calculate_reviewer_creduality()
        #self.analyze_products()

    def analyze_products(self):
        """
        Calls all product analysis functionality of REngine
        """
        logger.info('analyzing products information')
        print('* applying analysis to data')
        asins = self.utility_method.get_zero_rank_asins_from_db()
        if asins is not None:
            for asin in asins:
                try:
                    print(asin)
                    self.analyze_product(asin[0])
                    self.generate_product_triggers(asin[0])
                except Exception as e:
                    logger.exception(e.message)
        else:
            logger.error('something bad happened')

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

        reviews_text = self.utility_method.get_product_reviews_text_from_db(asin)
        reviews_length = []
        reviews_commons = []
        avg_review_length = 0
        try:
            if reviews_text:
                reviews_commons = self.find_common_phrases_in_reviews(reviews_text)
                for review_text in reviews_text:
                    blob = TextBlob(review_text[0].decode('utf-8'))
                    reviews_length.append(len(blob.words))
                avg_review_length = sum(reviews_length) / len(reviews_length)
        except Exception as e:
            logger.exception(e.message)

        try:
            for review in reviews:
                review_stats = {
                    "ReviewLink": review[0],
                    "ReviewLength": None,
                    "WordCountCategory": None,
                    "SentimentScore": None,
                    "SentimentLabel": None,
                    "CommonPhrase": None,
                    "CredulityScore": None,
                    "ReviewScore": None
                }

                try:
                    blob = TextBlob(review[3].decode('utf-8'))
                    review_stats["ReviewLength"] = len(blob.words)
                    logger.debug('ReviewLength: {length}'.format(length=review_stats["ReviewLength"]))
                    review_stats["SentimentScore"] = blob.sentiment.polarity * 100  # score between -100 to +100
                    review_stats["SentimentLabel"] = self.get_sentiment_label(review_stats["SentimentScore"])
                    review_stats["CredulityScore"] = self.utility_method.get_reviewer_creduality_from_db(review[5])[0][
                        0]
                    review_stats["WordCountCategory"] = self.get_word_count_category(avg_review_length, review_stats[
                        "ReviewLength"])
                    review_stats["CommonPhrase"] = self.is_most_common_phrase_exists(review[3].decode('utf-8'),
                                                                                     reviews_commons)
                    review_stats["ReviewScore"] = float(review[4]) + review_stats["SentimentScore"] + review_stats[
                        "CredulityScore"]
                except Exception as e:
                    logger.exception(e.message)
                self.utility_method.insert_rewiew_analysis_into_db(review_stats)
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

    def calculate_reviewer_creduality(self):
        """
        Calculates reviewer's credulity's and Participation histories
        """
        logger.debug('calculating reviewer creduality')
        try:
            reviewer_ids = self.utility_method.get_reviewers_ids_from_db()
            reviewer_data = {
                "ReviewerId": None,
                "TotalReviews": None,
                "CredualityScore": None,
                "ParticipationHistory": None
            }

            if reviewer_ids is not None:
                for reviewer_id in reviewer_ids:
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

                    if self.utility_method.update_reviewer_creduality_in_db(reviewer_data):
                        logger.debug('total reviews & creduality update success')
                    else:
                        logger.debug('error in updating creduality & total reviews')
            else:
                logger.debug('error in fetching reviewer ids from database')
        except Exception as e:
            logger.exception(e.message)

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

    def generate_product_triggers(self, product_asin):
        """
        Checks and generates all the triggers for product, reviews and reviewers
        :param product_asin: asin no of product
        """
        logger.debug('checking and generating triggers for product {asin}'.format(asin=product_asin))
        trigger_list = []
        try:
            over_lapping_review_trigger = self.triggers.get_overlapping_trigger(product_asin)
            wvc_trigger = self.triggers.get_words_vol_comparison_trigger(product_asin)
            rating_trend_trigger = self.triggers.get_rating_trend_trigger(product_asin)
            ts_ratio_trigger = self.triggers.get_three_star_ratio_check_trigger(product_asin)
            abnormal_review_trigger = self.triggers.get_abnormal_review_trigger(product_asin)
            review_spikes_trigger = self.triggers.get_review_spikes_trigger(product_asin)
            one_off_review_trigger = self.triggers.get_one_off_trigger()

            if over_lapping_review_trigger:
                trigger_list.append(1)
            if wvc_trigger:
                trigger_list.append(1)
            if rating_trend_trigger:
                trigger_list.append(1)
            if ts_ratio_trigger:
                trigger_list.append(1)
            if abnormal_review_trigger:
                trigger_list.append(0.5)
            if review_spikes_trigger:
                trigger_list.append(1)
            if one_off_review_trigger:
                trigger_list.append(1)

            try:
                reviewer_ids = self.utility_method.get_reviews_reviewer_ids_from_db(product_asin)
                for reviewer_id in reviewer_ids:
                    status = self.generate_reviewer_reliability_status(reviewer_id[0], trigger_list)
                    review_links = self.utility_method.get_review_ids_of_reviewer_from_db(reviewer_id[0])

                    for link in review_links:
                        try:
                            review_score = self.utility_method.get_review_score_from_db(link[0])[0][0]
                            if self.get_repeated_remarks_trigger(link[0], product_asin):
                                trigger_list.append(1)
                            updated_score = self.get_review_score(int(review_score), status)
                            self.utility_method.update_review_score_in_db(link[0], updated_score)
                        except Exception as e:
                            logger.exception(e.message)

                reviews_score = 0
                product_score = self.utility_method.get_product_rank_from_db(product_asin)[0][0]
                product_reviews = self.utility_method.get_product_reviews_from_db(product_asin)
                for review in product_reviews:
                    try:
                        score = self.utility_method.get_review_score_from_db(review[0])[0][0]
                        reviews_score += score
                    except Exception as e:
                        logger.exception(e.message)
                product_score += reviews_score
                self.utility_method.update_product_rank_in_db(product_asin, product_score)
            except Exception as e:
                logger.exception(e.message)
        except Exception as e:
            logger.exception(e.message)

    def generate_reviewer_reliability_status(self, reviewer_id, trigger_list):
        """
        Returns a reviewer's reliability status based on trigger list
        :param reviewer_id: id of reviewer
        :param trigger_list: activated triggers list
        :return: reliability status of reviewer
        """
        logger.debug('generating reviewer {reviewer_id} reliability status'.format(reviewer_id=reviewer_id))
        try:
            msd_reviews_trigger = self.triggers.get_multiple_single_day_reviews_trigger(reviewer_id)
            duplicated_reviews_trigger = self.triggers.get_duplicated_reviews_trigger(reviewer_id)

            if msd_reviews_trigger:
                trigger_list.append(1)
            if duplicated_reviews_trigger:
                trigger_list.append(1)

            total_triggers = len(trigger_list)
            if total_triggers >= 6:
                return 'RED'
            elif total_triggers in range(2, 5):
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

    def avg_word_len_category(self):
        categories = self.utility_method.get_distinct_category_from_products()
        for category in categories:
            AvgLength = {
                    "CategeoryName": None,
                    "AvgWordLength": None,
                    "NoOfProducts": None
                }
            reviews_length = []
            if not self.utility_method.check_category_in_avg_word_len(category[0]):
                product_asin = self.utility_method.get_product_asin_from_products(category[0])
                no_of_products = len(product_asin)
                for pa in product_asin:
                    reviews = self.utility_method.get_product_reviews(pa[0])
                    for review in reviews:
                        blob = TextBlob(review[0].decode('utf-8'))
                        reviews_length.append(len(blob.words))

                AvgLength["AvgWordLength"] = sum(reviews_length) / len(reviews_length)
                AvgLength["NoOfProducts"] = no_of_products
                AvgLength["CategeoryName"] = category[0]
                print(AvgLength)
                self.utility_method.insert_in_avg_word_len(AvgLength)
            else:
                print("not success yet")

    def word_volume_trigger(self):
        review_productasin = self.utility_method.get_reviewlength_productasin()
        for rp in review_productasin:
            print(rp[0], rp[1], rp[2])
            categories = self.utility_method.get_category_using_productasin(rp[1])
            for category in categories:
                avg_review_length = self.utility_method.get_avg_word_length(category[0])
                print (avg_review_length)
                trigger = ""
                if avg_review_length:
                    if int(rp[0]) < 0.2 * avg_review_length[0][0] or int(rp[0]) > 2.5 * avg_review_length[0][0]:
                        trigger = '1'
                        self.utility_method.insert_trigger_in_review_analysis(trigger, rp[2])
                    else:
                        trigger = '0'
                        self.utility_method.insert_trigger_in_review_analysis(trigger, rp[2])
                print (trigger)

    def get_abnormal_reviews(self):
        distinct_product_asin = self.utility_method.get_distinct_product_asin()
        
        for product_asin in distinct_product_asin:
            ProductAnalysis = {
                "ProductAsin": None,
                "TotatReviews": None,
                "TotalReviewsScraped": None,
                "MaxDate": None,
                "MinDate": None,
                "NoOf5star": None,
                "NoOf4star": None,
                "NoOf3star": None,
                "NoOf2star": None,
                "NoOf1star": None,
                "trigger": None
            }
            rating = self.utility_method.get_all_rating_stars(product_asin[0])
            print (rating)
            r_5 = 0
            r_4 = 0
            r_3 = 0
            r_2 = 0
            r_1 = 0
            try:
                for rate in rating:
                    if math.floor(rate[0]) == 5.0:
                        r_5 += 1
                    elif math.floor(rate[0]) == 4.0:
                        r_4 += 1
                    elif math.floor(rate[0]) == 3.0:
                        r_3 += 1
                    elif math.floor(rate[0]) == 2.0:
                        r_2 += 1
                    elif math.floor(rate[0]) == 1.0:
                        r_1 += 1
                    else:
                        continue
            except Exception as e:
                print(e.message)
            counttext_max_min_date = self.utility_method.get_min_max_date(product_asin[0])
            
            ProductAnalysis["ProductAsin"] = product_asin
            ProductAnalysis["TotatReviews"] = (counttext_max_min_date[0][0])
            ProductAnalysis["TotalReviewsScraped"] = (counttext_max_min_date[0][1])
            ProductAnalysis["MaxDate"] = (counttext_max_min_date[0][2])
            ProductAnalysis["MinDate"] = (counttext_max_min_date[0][3])
            ProductAnalysis["NoOf1star"] = r_1
            ProductAnalysis["NoOf2star"] = r_2
            ProductAnalysis["NoOf3star"] = r_3
            ProductAnalysis["NoOf4star"] = r_4
            ProductAnalysis["NoOf5star"] = r_5
            if ProductAnalysis["NoOf3star"] or ProductAnalysis["NoOf2star"] or ProductAnalysis["NoOf1star"]:
                trigger = '0'
            else:
                trigger = '1'
            ProductAnalysis["trigger"] = trigger
            self.utility_method.insert_in_abnormal_review_table(ProductAnalysis)
            print(ProductAnalysis)



    ######### Temporary ########

    def insert_status(self):
        product_asin = self.utility_method.get_distinct_product_asin()
        for product in product_asin:
            total_reviews = self.utility_method.get_total_reviews(product[0])[0][0].replace(',', '')
            scraped_reviews = self.utility_method.get_total_scraped(product[0])[0][0]
            print (total_reviews, scraped_reviews)
            global percent_scraped_reviews
            global status
            if total_reviews is not None and scraped_reviews is not None:
                if not total_reviews == 0:
                    percent_scraped_reviews = (float(scraped_reviews) / float(total_reviews)) * 100
            # if status == 0 which means it need to be scraped and if status == 1 which means no need to be scraped
            if 0 <= int(total_reviews) <= 100:
                logger.debug('checking if scraped reviews are more then 90%')
                if percent_scraped_reviews >= 50:
                    logger.debug('scraped reviews >= 90% True')
                    status = 1
                    self.utility_method.update_status(product[0], status)
                else:
                    logger.debug('scraped reviews >= 90% False')
                    status = 0
                    self.utility_method.update_status(product[0], status)

            elif 101 <= int(total_reviews) <= 1000:
                logger.debug('checking if scraped reviews are more then 50%')
                if percent_scraped_reviews >= 20:
                    logger.debug('scraped reviews >= 50% True')
                    status = 1
                    self.utility_method.update_status(product[0], status)
                else:
                    logger.debug('scraped reviews >= 50% False')
                    status = 0
                    self.utility_method.update_status(product[0], status)
            elif 1001 <= int(total_reviews) <= 5000:
                logger.debug('checking if scraped reviews are more then 25%')
                if percent_scraped_reviews >= 1:
                    logger.debug('scraped reviews >= 25% True')
                    status = 1
                    self.utility_method.update_status(product[0], status)
                else:
                    logger.debug('scraped reviews >= 25% False')
                    status = 0
                    self.utility_method.update_status(product[0], status)
            elif 5001 <= int(total_reviews) <= 10000:
                logger.debug('checking if scraped reviews are more then 10%')
                if percent_scraped_reviews >= 0.5:
                    logger.debug('scraped reviews >= 10% True')
                    status = 1
                    self.utility_method.update_status(product[0], status)
                else:
                    logger.debug('scraped reviews >= 10% False')
                    status = 0
                    self.utility_method.update_status(product[0], status)
            else:
                logger.debug('checking if scraped reviews are more then 1%')
                if percent_scraped_reviews >= 0.7:
                    logger.debug('scraped reviews >= 1% True')
                    status = 1
                    self.utility_method.update_status(product[0], status)
                else:
                    logger.debug('scraped reviews >= 1% False')
                    status = 0
                    self.utility_method.update_status(product[0], status)


    ######## Temporary ########