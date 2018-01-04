import logging

from textblob import TextBlob
from utility import UtilityFunctions

logger = logging.getLogger(__name__)


class Triggers:
    def __init__(self):
        logger.debug('initializing triggers generator')
        self.utility_methods = UtilityFunctions()

    def get_overlapping_trigger(self, product_asin):
        logger.debug('generating overlapping reviews trigger')
        product_reviewers = self.utility_methods.get_reviewers_from_db(product_asin)

        for item in product_reviewers:
            if not float(item[0]) >= 4:
                product_reviewers.remove(item)

        all_product_reviewers = self.utility_methods.get_all_reviewers_from_db(product_asin)
        count = 0  # TODO: Consider 4 to 5 star reviews only, need change in DB as well
        for reviewer in product_reviewers:
            for reviewers in all_product_reviewers:
                if reviewer in reviewers:
                    count += 1

        if count >= 10:
            return True
        else:
            return False

    def get_words_vol_comparison_trigger(self, product_asin):
        logger.debug('generating words volume comparison trigger')
        reviews_length = []
        reviews_text = self.utility_methods.get_product_reviews_text_from_db(product_asin)
        if reviews_text:
            for review_text in reviews_text:
                blob = TextBlob(review_text[0].decode('utf-8'))
                reviews_length.append(len(blob.words))
        avg_review_length = sum(reviews_length) / len(reviews_length)

        trigger = False
        for review_text in reviews_text:  # TODO: Consider 4-5 star reviews only, need change in database schema
            blob = TextBlob(review_text[0].decode('utf-8'))
            if len(blob.words) < 0.25*avg_review_length or len(blob.words) > 2*avg_review_length:
                trigger = True

        return trigger

    def get_one_off_trigger(self, reviewer_id): # TODO: Need to develop it
        logger.debug('generating one off reviewer trigger for {reviewer}'.format(reviewer=reviewer_id))

    def get_multiple_single_day_reviews_trigger(self, product_asin):
        logger.debug('generating multiple single day reviews trigger for product {asin}'.format(asin=product_asin))


