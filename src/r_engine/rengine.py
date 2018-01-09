import logging
import nltk
import math

from nltk.util import ngrams
from utility import UtilityFunctions
from textblob import TextBlob
from triggers import Triggers

logger = logging.getLogger(__name__)


class REngine:
    def __init__(self):
        logger.debug('initiating AEngine')
        self.utility_method = UtilityFunctions()
        self.triggers = Triggers()

    def start_engine(self):
        """
        Starts the REngine to start the data analytics
        """
        logger.info('starting analysis engine')
        self.calculate_reviewer_creduality()
        self.analyze_products()

    def analyze_products(self):
        """
        Calls all product analysis functionality of REngine
        """
        logger.info('analyzing products information')
        asins = self.utility_method.get_products_asin_from_db()
        for asin in asins:
            self.analyze_product(asin[0])
            self.generate_product_triggers(asin[0])

    def analyze_product(self, asin):
        """
        Analyze and perform analytics on a single product's data
        :param asin: asin no of the product
        """
        logger.debug('analyzing product {asin}'.format(asin=asin))
        logger.debug('getting product reviews from database')
        product_reviews = self.utility_method.get_product_reviews_from_db(asin)
        self.analyze_reviews(product_reviews, asin)

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
        if reviews_text:
            reviews_commons = self.find_common_phrases_in_reviews(reviews_text)
            for review_text in reviews_text:
                blob = TextBlob(review_text[0].decode('utf-8'))
                reviews_length.append(len(blob.words))
            avg_review_length = sum(reviews_length) / len(reviews_length)

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
                review_stats["CredulityScore"] = self.utility_method.get_reviewer_creduality_from_db(review[5])[0][0]
                review_stats["WordCountCategory"] = self.get_word_count_category(avg_review_length, review_stats[
                    "ReviewLength"])
                review_stats["CommonPhrase"] = self.is_most_common_phrase_exists(review[3].decode('utf-8'),
                                                                                 reviews_commons)
                review_stats["ReviewScore"] = float(review[4]) + review_stats["SentimentScore"] + review_stats[
                    "CredulityScore"]
            except Exception as e:
                logger.exception(e.message)

            self.utility_method.insert_rewiew_analysis_into_db(review_stats)

    @staticmethod
    def get_sentiment_label(sentiment_score):
        """
        Returns sentiment label for a sentiment score
        :param sentiment_score: sentiment score of text
        :return: sentiment label
        """
        logger.debug('generating sentiment label')

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

    @staticmethod
    def get_word_count_category(avg_review_length, review_length):
        """
        Returns Word-Count-Category of a review
        :param avg_review_length: average review length of a product
        :param review_length: length of the target review
        :return: Word Count Category
        """
        logger.debug('generating word count category')
        if 0 * avg_review_length <= review_length <= 0.25 * avg_review_length:
            return "A"
        elif 0.25 * avg_review_length <= review_length <= 2 * review_length:
            return "B"
        elif 2 * avg_review_length <= review_length:
            return "C"
        else:
            return "Error"

    def calculate_reviewer_creduality(self):
        """
        Calculates reviewer's credulity's and Participation histories
        """
        logger.debug('calculating reviewer creduality')
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

                reviewer_data["CredualityScore"] = sum_rates / float(reviewer_data["TotalReviews"]) if reviewer_data[
                    "TotalReviews"] else 0
                reviewer_data["ParticipationHistory"] = self.utility_method.calculate_participation_history(
                    reviewer_data["TotalReviews"])

                if self.utility_method.update_reviewer_creduality_in_db(reviewer_data):
                    logger.debug('total reviews & creduality update success')
                else:
                    logger.debug('error in updating creduality & total reviews')
        else:
            logger.debug('error in fetching reviewer ids from database')

    @staticmethod
    def find_common_phrases_in_reviews(reviews):
        """
        Finds and returns most common phrases in reviews of a product
        :param reviews: list of reviews
        :return: list of most common phrases
        """
        logger.debug('finding common phrases in reviews {reviews}'.format(reviews=reviews))
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

    @staticmethod
    def is_most_common_phrase_exists(review, reviews_commons):
        """
        Checks if a most common phrase exists in target review
        :param review: target review
        :param reviews_commons: list of common phrases in reviews
        :return: bool (True/False)
        """
        logger.debug('checking if most common phrase also found in most common phrases of reviews')

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
        Returns no of reviews which have most common phrase in them
        :param reviews: list of reviews
        :return: no of reviews & percentage reviews having most common phrase
        """
        logger.debug('finding common phrases in reviews {reviews}'.format(reviews=reviews))
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

    def generate_product_triggers(self, product_asin):
        logger.debug('checking and generating triggers for product {asin}'.format(asin=product_asin))
        trigger_list = []

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
                    review_score = self.utility_method.get_review_score_from_db(link[0])[0][0]
                    updated_score = self.get_review_score(int(review_score), status)
                    self.utility_method.update_review_score_in_db(link[0], updated_score)

            reviews_score = 0
            product_score = self.utility_method.get_product_rank_from_db(product_asin)[0][0]
            product_reviews = self.utility_method.get_product_reviews_from_db(product_asin)
            for review in product_reviews:
                score = self.utility_method.get_review_score_from_db(review[0])[0][0]
                reviews_score += score
            product_score += reviews_score
            self.utility_method.update_product_rank_in_db(product_asin, product_score)
        except Exception as e:
            logger.exception(e.message)

    def generate_reviewer_reliability_status(self, reviewer_id, trigger_list):
        logger.debug('generating reviewer {reviewer_id} reliability status'.format(reviewer_id=reviewer_id))

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

    @staticmethod
    def get_review_score(score, reviewer_status):
        logger.debug('calculating review score')

        if reviewer_status == 'GREEN':
            return score + 60
        elif reviewer_status == 'YELLOW':
            return score + 30
        elif reviewer_status == 'RED':
            return score - 60
