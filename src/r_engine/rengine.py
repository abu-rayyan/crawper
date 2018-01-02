import logging
import time

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

        for review in product_reviews:
            self.analyze_review(review)

    def analyze_review(self, review):
        logger.debug('analyzing review {review}'.format(review=review))

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

        blob = TextBlob(review[3].decode('utf-8'))
        review_stats["ReviewLength"] = len(blob.words)
        logger.debug('ReviewLength: {length}'.format(length=review_stats["ReviewLength"]))
        review_stats["SentimentScore"] = blob.sentiment.polarity * 100  # score between -100 to +100
        review_stats["SentimentLabel"] = self.get_sentiment_label(review_stats["SentimentScore"])
        review_stats["CredulityScore"] = 5  # TODO: Remove hard-coded value
        review_stats["WordCountCategory"] = "B"  # TODO: Remove hard-coded value
        review_stats["CommonPhrase"] = True  # TODO: Remove hard-coded value
        review_stats["ReviewScore"] = float(review[4]) + review_stats["SentimentScore"] + review_stats["CredulityScore"]

        self.utility_method.insert_rewiew_analysis_into_db(review_stats)


    def get_sentiment_label(self, sentiment_score):
        logger.debug('generating sentiment label')

        if -100 <= sentiment_score < -50:
            return 'angry'
        elif -50 <= sentiment_score < -10:
            return 'dissatisfied'
        elif -10 <= sentiment_score < 10:
            return 'neutral'
        elif 10 <= sentiment_score < 50:
            return 'satisfied'
        elif 50 <= sentiment_score <= 100 :
            return 'happy'
        else:
            return None