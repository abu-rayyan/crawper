import logging
import nltk
import math

from nltk.util import ngrams
from utility import UtilityFunctions
from textblob import TextBlob

logger = logging.getLogger(__name__)


class REngine:
    def __init__(self):
        logger.debug('initiating AEngine')
        self.utility_method = UtilityFunctions()

    def start_engine(self):
        logger.info('starting analysis engine')
        self.analyze_products()

    def analyze_products(self):
        logger.info('analyzing products information')
        asins = self.utility_method.get_products_asin_from_db()
        for asin in asins:
            self.analyze_product(asin[0])

    def analyze_product(self, asin):
        logger.debug('analyzing product {asin}'.format(asin=asin))
        logger.debug('getting product reviews from database')
        product_reviews = self.utility_method.get_product_reviews_from_db(asin)
        self.analyze_reviews(product_reviews, asin)

    def analyze_reviews(self, reviews, asin):
        logger.debug('analyzing reviews {review}'.format(review=reviews))

        reviews_text = self.utility_method.get_product_reviews_text_from_db(asin)
        reviews_length = []
        avg_review_length = 0
        if reviews_text:
            self.find_common_phrases_in_reviews(reviews_text)
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
                review_stats["CommonPhrase"] = True  # TODO: Remove hard-coded value
                review_stats["ReviewScore"] = float(review[4]) + review_stats["SentimentScore"] + review_stats[
                    "CredulityScore"]
            except Exception as e:
                logger.exception(e.message)

            self.utility_method.insert_rewiew_analysis_into_db(review_stats)

    @staticmethod
    def get_sentiment_label(sentiment_score):
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
        logger.debug('calculating reviewer creduality')
        reviewer_ids = self.utility_method.get_reviewers_ids_from_db()
        reviewer_data = {
            "ReviewerId": None,
            "TotalReviews": None,
            "CredualityScore": None
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

                if self.utility_method.update_reviewer_creduality_in_db(reviewer_data):
                    logger.debug('total reviews & creduality update success')
                else:
                    logger.debug('error in updating creduality & total reviews')
        else:
            logger.debug('error in fetching reviewer ids from database')

    @staticmethod
    def find_common_phrases_in_reviews(reviews):
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
